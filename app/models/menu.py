from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Sequence, Any, Dict

class BaseMenu(BaseModel):
    name: str = Field(..., title='image title')
    description: Optional[str] = Field(None, title='optional description')
    file_id: UUID = Field(..., title='image file id')

class MenuAddVM(BaseMenu):
    pass

class MenuUpdateVM(BaseMenu):
    pass

class Menu(BaseMenu):
    id: UUID = Field(..., title='id')
