from typing import Optional, Sequence, Dict, Any, Mapping
from databases import Database
from uuid import UUID
import json

from app.models.ingredient import Ingredient, IngredientAddVM, IngredientUpdateVM
from app.data.utils import build_insert_stmts, build_update_stmt, map_dict


class IngredientData:
    key_map = {
        'text': 'ingr_text',
        'order': 'ingr_order'
    }

    def __init__(self, db: Database) -> None:
        self.db = db

    def _map_record_to_model(self, record: Mapping[Any, Any]) -> Optional[Ingredient]:
        if not record:
            return None

        mapped_dict = map_dict(
            to_be_mapped=dict(record),
            key_map=self.key_map,
            json_fields=None,
            reverse=True
        )
        return Ingredient(**mapped_dict)

    async def get_recipe_ingredients(self, recipe_id: UUID) -> Sequence[Ingredient]:
        records = await self.db.fetch_all(
            query="""
                SELECT * FROM ingredients
                WHERE recipe_id = :recipe_id
            """,
            values={'recipe_id': recipe_id}
        )
        return [self._map_record_to_model(record=record) for record in records]

    async def get(self, id: UUID) -> Optional[Ingredient]:
        record = await self.db.fetch_one(
            query="""
                SELECT * FROM ingredients
                WHERE id = :id;
            """,
            values={'id': id}
        )
        return self._map_record_to_model(record=record)

    async def add(self, ingredient: Ingredient) -> UUID:
        mapped_dict = ingredient.dict()
        values = mapped_dict
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)

        return await self.db.execute(
            query=f"""
                INSERT INTO ingredients({fields_stmt})
                VALUES({values_stmt});
            """,
            values=values
        )

    async def delete(self, id: UUID) -> int:
        return await self.db.fetch_val(
            query=f'''
                WITH delete_item as (
                    DELETE FROM ingredients
                    WHERE id = :id
                    RETURNING *
                )
                SELECT COUNT(*) as deleted FROM delete_item;
            ''',
            values = {'id': id},
            column='deleted'
        )

    async def update(self, id: UUID, ingredient: Ingredient) -> int:
        mapped_dict = ingredient.dict(exclude={'id'})
        update_stmt = build_update_stmt(mapped_dict=mapped_dict)
        values = mapped_dict
        values['id'] = id

        updated = await self.db.fetch_val(
            query=f'''
                WITH update_item as (
                    UPDATE ingredients
                    SET {update_stmt}
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated FROM update_item;
            ''',
            values=values,
            column='updated'
        )
        return updated
