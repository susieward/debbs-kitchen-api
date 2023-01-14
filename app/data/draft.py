from typing import Optional, Sequence, Dict, Any, Mapping
from databases import Database
from uuid import UUID

from app.models.draft import Draft, DraftAddVM, DraftUpdateVM
from app.data.utils import build_insert_stmts, build_update_stmt, map_dict

class DraftData:
    json_fields = ['ingredients', 'instructions', 'tags']

    def __init__(self, db: Database) -> None:
        self.db = db

    def _map_record_to_model(record: Mapping[Any, Any]) -> Optional[Draft]:
        if not record:
            return None

        mapped_dict = map_dict(
            to_be_mapped=dict(record),
            key_map={},
            json_fields=self.json_fields
        )
        return Draft(**mapped_dict)

    async def get_list(self):
        query = "SELECT * FROM drafts"
        records = await self.db.fetch_all(query=query)
        return [self._map_record_to_model(record=record) for record in records]

    async def get(self, id: UUID) -> Optional[Draft]:
        record = await self.db.fetch_one(
            query="""
                SELECT * FROM drafts
                WHERE id = :id;
            """,
            values={'id': id}
        )
        return self._map_record_to_model(record=record)

    async def add(self, draft: Draft) -> UUID:
        mapped_dict = draft.dict()
        values = mapped_dict
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)

        return await self.db.execute(
            query=f"""
                INSERT INTO drafts({fields_stmt})
                VALUES({values_stmt});
            """,
            values=values
        )

    async def delete(self, id: UUID) -> int:
        return await self.db.fetch_val(
            query=f'''
                WITH delete_item as (
                    DELETE FROM drafts
                    WHERE id = :id RETURNING *
                )
                SELECT COUNT(*) as deleted FROM delete_item;
            ''',
            values = {'id': id},
            column='deleted'
        )

    async def update(self, id: UUID, draft: Draft) -> int:
        mapped_dict = draft.dict(exclude={'id'})
        update_stmt = build_update_stmt(mapped_dict=mapped_dict)
        values = mapped_dict
        values['id'] = id

        updated = await self.db.fetch_val(
            query=f'''
                WITH update_item as (
                    UPDATE drafts
                    SET {update_stmt}
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated FROM update_item;
            ''',
            values=values,
            column='updated'
        )
        return updated
