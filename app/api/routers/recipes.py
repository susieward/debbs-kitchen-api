from uuid import UUID
import json

from fastapi import APIRouter, Path, Body, Depends, HTTPException, Request, Response
from starlette import status

from app.api.dependencies import recipe_logic_dep
from app.logic.recipe import RecipeLogic
from app.models.recipe import Recipe, RecipeAddVM, RecipeUpdateVM

from app.models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.get('/recipes')
async def get_recipes(recipe_logic: RecipeLogic = Depends(recipe_logic_dep)):
    try:
        return await recipe_logic.get_list()
    except Exception as e:
        print(e)
        msg = f"{e}"
        raise HTTPException(status_code=500, detail = msg)


@router.get('/recipe/{id}', response_model=Recipe)
async def get_recipe(
    recipe_logic: RecipeLogic = Depends(recipe_logic_dep),
    id: UUID = Path(...)
):
    recipe = await recipe_logic.get(id=id)
    return recipe


@router.post('/recipe', response_model=AddResponse, status_code=status.HTTP_201_CREATED)
async def add_recipe(
    recipe_logic: RecipeLogic = Depends(recipe_logic_dep),
    recipe_vm: RecipeAddVM = Body(...)
):
    id = await recipe_logic.add(recipe_vm=recipe_vm)
    return AddResponse(id=id)


@router.put('/recipe/{id}', response_model=UpdateResponse)
async def update_recipe(
    recipe_logic: RecipeLogic = Depends(recipe_logic_dep),
    id: UUID = Path(...),
    recipe_vm: RecipeUpdateVM = Body(...)
):
    updated = await recipe_logic.update(id=id, recipe_vm=recipe_vm)
    return UpdateResponse(updated=updated)


@router.delete('/recipe/{id}', response_model=DeleteResponse)
async def delete_recipe(
    recipe_logic: RecipeLogic = Depends(recipe_logic_dep),
    id: UUID = Path(...)
):
    deleted = await recipe_logic.delete(id=id)
    return DeleteResponse(deleted=deleted)
