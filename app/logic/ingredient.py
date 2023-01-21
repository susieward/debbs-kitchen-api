from typing import Optional, Sequence, Dict, Any, Mapping
from uuid import UUID, uuid4

from app.data.ingredient import IngredientData
from app.api.exceptions import NotFoundError
from app.models.ingredient import Ingredient, IngredientAddVM, IngredientUpdateVM


class IngredientLogic:
    def __init__(self, ingredient_data: IngredientData) -> None:
        self._ingredient_data = ingredient_data

    async def get_recipe_ingredients(self, recipe_id: UUID) -> Sequence[Ingredient]:
        return await self._ingredient_data.get_recipe_ingredients(recipe_id=recipe_id)

    async def get(self, id: UUID) -> Optional[Ingredient]:
        ingredient = await self._ingredient_data.get(id=id)
        if not ingredient:
            raise NotFoundError(resource_type=Ingredient.__name__, resource_id=id)

        return ingredient

    async def add(self, ingredient_vm: IngredientAddVM) -> UUID:
        ingredient = Ingredient(id=uuid4(), **ingredient_vm.dict())
        await self._ingredient_data.add(ingredient=ingredient)
        return ingredient.id

    async def update(self, id: UUID, ingredient_vm: IngredientUpdateVM) -> int:
        rows = 0
        ingredient = await self._ingredient_data.get(id=id)

        for name, val in ingredient_vm:
            setattr(ingredient, name, val)

        rows = await self._ingredient_data.update(id=id, ingredient=ingredient)
        return rows

    async def delete(self, id: UUID) -> int:
        return await self._ingredient_data.delete(id=id)
