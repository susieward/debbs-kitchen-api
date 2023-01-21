from typing import Optional, Sequence
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.data.instruction import InstructionData
from app.api.exceptions import NotFoundError
from app.models.instruction import Instruction, InstructionAddVM, InstructionUpdateVM


class InstructionLogic:
    def __init__(self, instruction_data: InstructionData) -> None:
        self._instruction_data = instruction_data

    async def get_recipe_instructions(self, recipe_id: UUID) -> Sequence[Instruction]:
        return await self._instruction_data.get_recipe_instructions(recipe_id=recipe_id)

    async def get(self, id: UUID) -> Optional[Instruction]:
        instruction = await self._instruction_data.get(id=id)
        if not instruction:
            raise NotFoundError(resource_type=Instruction.__name__, resource_id=id)

        return instruction

    async def add(self, instruction_vm: InstructionAddVM) -> UUID:
        new_timestamp = datetime.now(timezone.utc)
        instruction = Instruction(
            id=uuid4(),
            created_on=new_timestamp,
            updated_on=new_timestamp,
            **instruction_vm.dict()
        )
        await self._instruction_data.add(instruction=instruction)
        return instruction.id

    async def update(self, id: UUID, instruction_vm: InstructionUpdateVM) -> int:
        rows = 0
        instruction = await self._instruction_data.get(id=id)

        for name, val in instruction_vm:
            setattr(instruction, name, val)

        rows = await self._instruction_data.update(id=id, instruction=instruction)
        return rows

    async def delete(self, id: UUID) -> int:
        return await self._instruction_data.delete(id=id)
