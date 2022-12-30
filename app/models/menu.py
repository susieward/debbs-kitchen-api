from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Sequence, Any, Dict

class BaseMenu(BaseModel):
    date: int = Field(..., title='menu date')
    month: str = Field(..., title='menu month')
    year: str = Field(..., title='menu year')
    dishes: Optional[Sequence[Dict[str, Any]]] = Field(None, title='dishes array')

class MenuAddVM(BaseMenu):
    pass

class MenuUpdateVM(BaseMenu):
    pass

class Menu(BaseMenu):
    id: UUID = Field(..., title='id')
