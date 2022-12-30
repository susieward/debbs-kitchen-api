from typing import Optional, Sequence, Dict, Any, Mapping
from databases import Database
from uuid import UUID
import json

from app.models.recipe import Recipe, RecipeAddVM, RecipeUpdateVM
from app.data.utils import build_insert_stmts, build_update_stmt, map_dict


class RecipeData:
    json_fields = ['ingredients', 'instructions', 'tags']

    def __init__(self, db: Database) -> None:
        self.db = db

    def _map_record_to_model(self, record: Mapping[Any, Any]) -> Optional[Recipe]:
        if not record:
            return None

        mapped_dict = map_dict(
            to_be_mapped=dict(record),
            key_map={},
            json_fields=self.json_fields
        )
        return Recipe(**mapped_dict)

    async def get_list(self):
        query = "SELECT * FROM recipes"
        records = await self.db.fetch_all(query=query)
        return [self._map_record_to_model(record=record) for record in records]

    async def get(self, id: UUID) -> Optional[Recipe]:
        record = await self.db.fetch_one(
            query="""
                SELECT * FROM recipes
                WHERE id = :id;
            """,
            values={'id': id}
        )
        return self._map_record_to_model(record=record)

    async def add(self, recipe: Recipe) -> UUID:
        mapped_dict = recipe.dict()
        values = mapped_dict
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)

        return await self.db.execute(
            query=f"""
                INSERT INTO recipes({fields_stmt})
                VALUES({values_stmt});
            """,
            values=values
        )

    async def delete(self, id: UUID) -> int:
        return await self.db.fetch_val(
            query=f'''
                WITH delete_item as (
                    DELETE FROM recipes
                    WHERE id = :id RETURNING *
                )
                SELECT COUNT(*) as deleted FROM delete_item;
            ''',
            values = {'id': id},
            column='deleted'
        )

    async def update(self, id: UUID, recipe: Recipe) -> int:
        mapped_dict = recipe.dict(exclude={'id', 'ingredients', 'instructions', 'tags'})
        update_smt = build_update_stmt(mapped_dict=mapped_dict)
        values = mapped_dict
        values['id'] = id
        for field in self.json_fields:
            value = mapped_dict.get(field)
            if value:
                mapped_dict[field] = json.dumps(value)

        updated = await self.db.fetch_val(
            query=f'''
                WITH update_item as (
                    UPDATE recipes
                    SET {update_stmt}
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated FROM update_item;
            ''',
            values=values,
            column='updated'
        )
        return updated
