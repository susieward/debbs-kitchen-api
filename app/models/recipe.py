from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Sequence, Any, Dict, Union

class BaseRecipe(BaseModel):
    name: str = Field(..., title='name')
    ingredients: Optional[Sequence[Union[Dict, str]]] = Field(None, title='ingredients list')
    instructions: Optional[Sequence[Dict[str, Any]]] = Field(None, title='instructions list')
    tags: Optional[Sequence[str]] = Field(None, title='tags')
    photo: Optional[str] = Field(None, title='photo ref')

class RecipeAddVM(BaseRecipe):
    pass

class RecipeUpdateVM(BaseRecipe):
    pass

class Recipe(BaseRecipe):
    id: UUID = Field(..., title='id')