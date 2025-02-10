from typing import Union, Any
import random
import string
from datetime import datetime, timezone

from ..domain import Message
from ..repository import MessageRepo
from core.db.session_message import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class MessageService:
    async def create_message(self, device: str, sender: str, target: str, text: str) -> Message:
        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_create = Message.create(
                    device=device,
                    sender=sender,
                    target=target,
                    text=text,
                )
                return await MessageRepo().save_message(db, data_create)

    async def get_message(self, message_id: int):
        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await MessageRepo().get_message(db, message_id)

    async def update_message(self, message_id: int, status: str = None, state: str = None) -> Message:
        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await MessageRepo().get_message(db, message_id)
                if data_get is None:
                    return False
                updates = {}
                if status is not None:
                    updates["status"] = status
                if state is not None:
                    updates["state"] = state
                return await MessageRepo().update_message(db, data_get, **updates)

    async def datatable_message(self, params: dict[str, Any]):
        from sqlalchemy import or_, select, case, literal, func
        from core.utils.datatables import DataTable

        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = select(
                    Message,
                    Message.id.label("DT_RowId"),
                ).order_by(Message.timestamp.desc())
                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=["DT_RowId", "id", "timestamp", "device", "sender", "target", "text", "status", "state"],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
