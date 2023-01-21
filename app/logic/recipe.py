from typing import Optional, Sequence, Dict, Any, Mapping
from uuid import UUID, uuid4

from app.data.recipe import RecipeData
from app.api.exceptions import NotFoundError
from app.models.recipe import Recipe, RecipeAddVM, RecipeUpdateVM


class RecipeLogic:
    def __init__(self, recipe_data: RecipeData) -> None:
        self._recipe_data = recipe_data

    async def get_list(self) -> Sequence[Recipe]:
        return await self._recipe_data.get_list()

    async def get(self, id: UUID) -> Optional[Recipe]:
        recipe = await self._recipe_data.get(id=id)
        if not recipe:
            raise NotFoundError(resource_type=Recipe.__name__, resource_id=id)

        return recipe

    async def add(self, recipe_vm: RecipeAddVM) -> UUID:
        recipe = Recipe(id=uuid4(), **recipe_vm.dict())
        await self._recipe_data.add(recipe=recipe)
        return recipe.id

    async def update(self, id: UUID, recipe_vm: RecipeUpdateVM) -> int:
        rows = 0
        recipe = await self._recipe_data.get(id=id)

        for name, val in recipe_vm:
            setattr(recipe, name, val)

        rows = await self._recipe_data.update(id=id, recipe=recipe)
        return rows

    async def delete(self, id: UUID) -> int:
        return await self._recipe_data.delete(id=id)
