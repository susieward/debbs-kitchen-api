from uuid import UUID
import json

from fastapi import APIRouter, Path, Body, Depends, HTTPException, Request, Response
from starlette import status

from app.api.dependencies import draft_logic_dep
from app.logic.draft import DraftLogic
from app.models.draft import Draft, DraftAddVM, DraftUpdateVM

from app.models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.get('/drafts')
async def get_drafts(draft_logic: DraftLogic = Depends(draft_logic_dep)):
    try:
        return await draft_logic.get_list()
    except Exception as e:
        print(e)
        msg = f"{e}"
        raise HTTPException(status_code=500, detail = msg)


@router.get('/draft/{id}', response_model=Draft)
async def get_draft(
    draft_logic: DraftLogic = Depends(draft_logic_dep),
    id: UUID = Path(...)
):
    recipe = await draft_logic.get(id=id)
    return recipe


@router.post('/draft', response_model=AddResponse, status_code=status.HTTP_201_CREATED)
async def add_draft(
    draft_logic: DraftLogic = Depends(draft_logic_dep),
    draft_vm: DraftAddVM = Body(...)
):
    id = await draft_logic.add(draft_vm=draft_vm)
    return AddResponse(id=id)


@router.put('/draft/{id}', response_model=UpdateResponse)
async def update_draft(
    draft_logic: DraftLogic = Depends(draft_logic_dep),
    id: UUID = Path(...),
    draft_vm: DraftUpdateVM = Body(...)
):
    updated = await draft_logic.update(id=id, draft_vm=draft_vm)
    return UpdateResponse(updated=updated)


@router.delete('/draft/{id}', response_model=DeleteResponse)
async def delete_draft(
    draft_logic: DraftLogic = Depends(draft_logic_dep),
    id: UUID = Path(...)
):
    deleted = await draft_logic.delete(id=id)
    return DeleteResponse(deleted=deleted)
