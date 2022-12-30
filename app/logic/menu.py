from typing import Optional, Sequence, Dict, Any, Mapping
from uuid import UUID, uuid4

from app.data.menu import MenuData
from app.exceptions import NotFoundError
from app.models.menu import Menu, MenuAddVM, MenuUpdateVM


class MenuLogic:
    def __init__(self, menu_data: MenuData) -> None:
        self._menu_data = menu_data

    async def get_list(self) -> Sequence[Menu]:
        return await self._menu_data.get_list()

    async def get(self, id: UUID) -> Optional[Menu]:
        menu = await self._menu_data.get(id=id)
        if not menu:
            raise NotFoundError(resource_type=Menu.__name__, resource_id=id)

        return menu

    async def add(self, menu_vm: MenuAddVM) -> UUID:
        menu = Menu(id=uuid4(), **menu_vm.dict())
        await self._menu_data.add(menu=menu)
        return menu.id

    async def update(self, id: UUID, menu_vm: MenuUpdateVM) -> int:
        rows = 0
        menu = await self._menu_data.get(id=id)

        for name, val in menu_vm:
            setattr(menu, name, val)

        rows = await self._menu_data.update(id=id, menu=menu)
        return rows

    async def delete(self, id: UUID) -> int:
        return await self._menu_data.delete(id=id)
