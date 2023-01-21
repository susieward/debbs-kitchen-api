from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class BaseIngredient(BaseModel):
    text: str = Field(..., title='text')
    order: int = Field(..., title='order')
    recipe_id: UUID = Field(..., title='recipe id')

class IngredientAddVM(BaseIngredient):
    pass

class IngredientUpdateVM(BaseIngredient):
    pass

class Ingredient(BaseIngredient):
    id: UUID = Field(..., title='id')
    created_on: datetime = Field(..., title='created on')
    updated_on: datetime = Field(..., title='updated on')
