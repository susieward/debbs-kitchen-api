from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Sequence, Any, Dict, Union

from app.models.instruction import Instruction
from app.models.ingredient import Ingredient

class BaseRecipe(BaseModel):
    name: str = Field(..., title='name')
    tags: Optional[Sequence[str]] = Field(None, title='tags')
    photo: Optional[str] = Field(None, title='photo ref')

class RecipeAddVM(BaseRecipe):
    pass

class RecipeUpdateVM(BaseRecipe):
    pass

class Recipe(BaseRecipe):
    id: UUID = Field(..., title='id')

class RecipeExpanded(Recipe):
    ingredients: Optional[Sequence[Ingredient]] = Field(None, title='ingredients list')
    instructions: Optional[Sequence[Instruction]] = Field(None, title='instructions list')
