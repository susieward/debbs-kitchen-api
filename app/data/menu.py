from typing import Optional, Sequence, Dict, Any, Mapping
from databases import Database
from uuid import UUID, uuid4
import json

from app.models.menu import Menu, MenuAddVM, MenuUpdateVM
from app.data.utils import build_insert_stmts, build_update_stmt, map_dict


class MenuData:
    key_map = {
        'date': 'menu_date',
        'month': 'menu_month',
        'year': 'menu_year'
    }
    json_fields = ['dishes']

    def __init__(self, db: Database) -> None:
        self.db = db

    def _map_record_to_model(record: Mapping[Any, Any]) -> Optional[Menu]:
        if not record:
            return None

        mapped_dict = map_dict(
            to_be_mapped=dict(record),
            key_map=self.key_map,
            json_fields=self.json_fields,
            reverse=True
        )
        return Menu(**mapped_dict)

    async def get_list(self) -> Sequence[Menu]:
        query = "SELECT * FROM menus"
        records = await self.db.fetch_all(query=query)
        return [self._map_record_to_model(record=record) for record in records]

    async def get(self, id: UUID) -> Optional[Menu]:
        record = await self.db.fetch_one(
            query="""
                SELECT * FROM menus
                WHERE id = :id;
            """,
            values={'id': id}
        )
        return self._map_record_to_model(record=record)

    async def add(self, menu: Menu) -> UUID:
        mapped_dict = map_dict(
            to_be_mapped=menu.dict(),
            key_map=self.key_map
        )
        values = mapped_dict
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)
        for field in self.json_fields:
            value = mapped_dict.get(field)
            if value is not None:
                values[field] = json.dumps(value)

        return await self.db.execute(
            query=f"""
                INSERT INTO menus({fields_stmt})
                VALUES({values_stmt});
            """,
            values=values
        )

    async def delete(self, id: UUID) -> int:
        return await self.db.fetch_val(
            query=f'''
                WITH delete_item as (
                    DELETE FROM menus
                    WHERE id = :id RETURNING *
                )
                SELECT COUNT(*) as deleted FROM delete_item;
            ''',
            values = {'id': id},
            column='deleted'
        )

    async def update(self, id: UUID, menu: Menu) -> int:
        mapped_dict = map_dict(
            to_be_mapped=menu.dict(exclude={'id'}),
            key_map=self.key_map,
            json_fields=self.json_fields
        )
        update_smt = build_update_stmt(mapped_dict=mapped_dict)
        values = mapped_dict
        values['id'] = id
        for field in self.json_fields:
            value = mapped_dict.get(field)
            if value is not None:
                values[field] = json.dumps(value)

        updated = await self.db.fetch_val(
            query=f'''
                WITH update_item as (
                    UPDATE menus
                    SET {update_stmt}
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated FROM update_item;
            ''',
            values=values,
            column='updated'
        )
        return updated
