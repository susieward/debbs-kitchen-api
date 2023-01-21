from typing import Optional, Sequence, Dict, Any, Mapping, Union
from databases import Database
from uuid import UUID
import json
import asyncio

from app.models.recipe import Recipe, RecipeExpanded, RecipeAddVM, RecipeUpdateVM
from app.data.instruction import InstructionData
from app.data.ingredient import IngredientData
from app.data.utils import build_insert_stmts, build_update_stmt, map_dict


class RecipeData:
    json_fields = ['tags']

    def __init__(self, db: Database, instruction_data: InstructionData, ingredient_data: IngredientData) -> None:
        self.db = db
        self._instruction_data = instruction_data
        self._ingredient_data = ingredient_data

    async def _map_record_to_model(self, record: Mapping[Any, Any], expanded: bool = False) -> Optional[Union[RecipeExpanded, Recipe]]:
        if not record:
            return None

        mapped_dict = map_dict(
            to_be_mapped=dict(record),
            key_map={},
            json_fields=self.json_fields
        )

        if expanded:
            recipe_id = mapped_dict.get('id')
            instructions, ingredients = await asyncio.gather(
                self._instruction_data.get_recipe_instructions(recipe_id=recipe_id),
                self._ingredient_data.get_recipe_ingredients(recipe_id=recipe_id)
            )

            return RecipeExpanded(
                instructions=instructions,
                ingredients=ingredients,
                **mapped_dict
            )

        return Recipe(**mapped_dict)

    async def get_list(self):
        query = "SELECT * FROM recipes"
        records = await self.db.fetch_all(query=query)
        tasks = [self._map_record_to_model(record=record) for record in records]
        return await asyncio.gather(*tasks)

    async def get(self, id: UUID, expanded: bool = True) -> Optional[Union[Recipe, RecipeExpanded]]:
        record = await self.db.fetch_one(
            query="""
                SELECT * FROM recipes
                WHERE id = :id;
            """,
            values={'id': id}
        )
        return await self._map_record_to_model(record=record, expanded=expanded)

    async def add(self, recipe: Recipe) -> UUID:
        mapped_dict = recipe.dict()
        values = mapped_dict
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)
        for field in self.json_fields:
            value = mapped_dict.get(field)
            if value is not None:
                values[field] = json.dumps(value)

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
        mapped_dict = recipe.dict(exclude={'id'})
        update_stmt = build_update_stmt(mapped_dict=mapped_dict)
        values = mapped_dict
        values['id'] = id
        for field in self.json_fields:
            value = mapped_dict.get(field)
            if value is not None:
                values[field] = json.dumps(value)

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
