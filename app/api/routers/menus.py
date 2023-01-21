from uuid import UUID
from typing import Sequence, Optional
import json

from fastapi import APIRouter, Path, Body, Depends, HTTPException, Query
from starlette import status

from app.api.dependencies import menu_logic_dep
from app.logic.menu import MenuLogic
from app.models.menu import Menu, MenuAddVM, MenuUpdateVM

from app.models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

def error_handler(func):
    def with_detail(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{str(e)}')
    return with_detail

@error_handler
@router.get('/menus', response_model=Sequence[Menu])
async def get_menus(
    menu_logic: MenuLogic = Depends(menu_logic_dep),
    year: Optional[str] = Query(None),
    month: Optional[str] = Query(None)
):
    if year or month:
        return await menu_logic.get_by_year_month(year=year, month=month)

    return await menu_logic.get_list()

@error_handler
@router.get('/menu/{id}', response_model=Menu)
async def get_menu(
    menu_logic: MenuLogic = Depends(menu_logic_dep),
    id: UUID = Path(...)
):
    menu = await menu_logic.get(id=id)
    return menu

@error_handler
@router.post('/menu', response_model=AddResponse, status_code=status.HTTP_201_CREATED)
async def add_menu(
    menu_logic: MenuLogic = Depends(menu_logic_dep),
    menu_vm: MenuAddVM = Body(...)
):
    id = await menu_logic.add(menu_vm=menu_vm)
    return AddResponse(id=id)

@error_handler
@router.put('/menu/{id}', response_model=UpdateResponse)
async def update_menu(
    menu_logic: MenuLogic = Depends(menu_logic_dep),
    id: UUID = Path(...),
    menu_vm: MenuUpdateVM = Body(...)
):
    updated = await menu_logic.update(id=id, menu_vm=menu_vm)
    return UpdateResponse(updated=updated)

@error_handler
@router.delete('/menu/{id}', response_model=DeleteResponse)
async def delete_menu(
    menu_logic: MenuLogic = Depends(menu_logic_dep),
    id: UUID = Path(...)
):
    deleted = await menu_logic.delete(id=id)
    return DeleteResponse(deleted=deleted)
