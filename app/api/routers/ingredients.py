from uuid import UUID
from typing import Sequence

from fastapi import APIRouter, Path, Body, Depends, HTTPException
from starlette import status

from app.api.dependencies import ingredient_logic_dep
from app.logic.ingredient import IngredientLogic
from app.models.ingredient import Ingredient, IngredientAddVM, IngredientUpdateVM

from app.models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.get('/ingredients/{recipe_id}', response_model=Sequence[Ingredient])
async def get_ingredients(
    ingredient_logic: IngredientLogic = Depends(ingredient_logic_dep),
    recipe_id: UUID = Path(...)
):
    try:
        return await ingredient_logic.get_recipe_ingredients(recipe_id=recipe_id)
    except Exception as e:
        print(e)
        msg = f"{e}"
        raise HTTPException(status_code=500, detail=msg) from e


@router.get('/ingredient/{id}', response_model=Ingredient)
async def get_ingredient(
    ingredient_logic: IngredientLogic = Depends(ingredient_logic_dep),
    id: UUID = Path(...)
):
    ingredient = await ingredient_logic.get(id=id)
    return ingredient


@router.post('/ingredient', response_model=AddResponse, status_code=status.HTTP_201_CREATED)
async def add_ingredient(
    ingredient_logic: IngredientLogic = Depends(ingredient_logic_dep),
    ingredient_vm: IngredientAddVM = Body(...)
):
    id = await ingredient_logic.add(ingredient_vm=ingredient_vm)
    return AddResponse(id=id)


@router.put('/ingredient/{id}', response_model=UpdateResponse)
async def update_ingredient(
    ingredient_logic: IngredientLogic = Depends(ingredient_logic_dep),
    id: UUID = Path(...),
    ingredient_vm: IngredientUpdateVM = Body(...)
):
    updated = await ingredient_logic.update(id=id, ingredient_vm=ingredient_vm)
    return UpdateResponse(updated=updated)


@router.delete('/ingredient/{id}', response_model=DeleteResponse)
async def delete_ingredient(
    ingredient_logic: IngredientLogic = Depends(ingredient_logic_dep),
    id: UUID = Path(...)
):
    deleted = await ingredient_logic.delete(id=id)
    return DeleteResponse(deleted=deleted)
