from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class BaseInstruction(BaseModel):
    text: str = Field(..., title='text')
    order: int = Field(..., title='number/order')
    recipe_id: UUID = Field(..., title='recipe id')

class InstructionAddVM(BaseInstruction):
    pass

class InstructionUpdateVM(BaseInstruction):
    pass

class Instruction(BaseInstruction):
    id: UUID = Field(..., title='id')
    created_on: datetime = Field(..., title='created on')
    updated_on: datetime = Field(..., title='updated on')
