from uuid import UUID
from typing import Sequence

from fastapi import APIRouter, Path, Body, Depends, HTTPException
from starlette import status

from app.api.dependencies import instruction_logic_dep
from app.logic.instruction import InstructionLogic
from app.models.instruction import Instruction, InstructionAddVM, InstructionUpdateVM

from app.models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.get('/instructions/{recipe_id}', response_model=Sequence[Instruction])
async def get_instructions(
    instruction_logic: InstructionLogic = Depends(instruction_logic_dep),
    recipe_id: UUID = Path(...)
):
    try:
        return await instruction_logic.get_recipe_instructions(recipe_id=recipe_id)
    except Exception as e:
        print(e)
        msg = f"{e}"
        raise HTTPException(status_code=500, detail = msg) from e


@router.get('/instruction/{id}', response_model=Instruction)
async def get_instruction(
    instruction_logic: InstructionLogic = Depends(instruction_logic_dep),
    id: UUID = Path(...)
):
    instruction = await instruction_logic.get(id=id)
    return instruction


@router.post('/instruction', response_model=AddResponse, status_code=status.HTTP_201_CREATED)
async def add_instruction(
    instruction_logic: InstructionLogic = Depends(instruction_logic_dep),
    instruction_vm: InstructionAddVM = Body(...)
):
    id = await instruction_logic.add(instruction_vm=instruction_vm)
    return AddResponse(id=id)


@router.put('/instruction/{id}', response_model=UpdateResponse)
async def update_instruction(
    instruction_logic: InstructionLogic = Depends(instruction_logic_dep),
    id: UUID = Path(...),
    instruction_vm: InstructionUpdateVM = Body(...)
):
    updated = await instruction_logic.update(id=id, instruction_vm=instruction_vm)
    return UpdateResponse(updated=updated)


@router.delete('/instruction/{id}', response_model=DeleteResponse)
async def delete_instruction(
    instruction_logic: InstructionLogic = Depends(instruction_logic_dep),
    id: UUID = Path(...)
):
    deleted = await instruction_logic.delete(id=id)
    return DeleteResponse(deleted=deleted)