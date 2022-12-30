from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Sequence, Any, Dict, Union

class BaseDraft(BaseModel):
    name: str = Field(..., title='name')
    ingredients: Optional[Sequence[Union[Dict, str]]] = Field(None, title='ingredients list')
    instructions: Optional[Sequence[Dict[str, Any]]] = Field(None, title='instructions list')
    tags: Optional[Sequence[str]] = Field(None, title='tags')

class DraftAddVM(BaseDraft):
    pass

class DraftUpdateVM(BaseDraft):
    pass

class Draft(BaseDraft):
    id: UUID = Field(..., title='id')
