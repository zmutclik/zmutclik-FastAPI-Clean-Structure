from typing import Union, Any
import random
import string
from datetime import datetime

from ..domain import Session
from ..repository import SessionRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class SessionService:
    async def __generate_new_session(self, db: AsyncSession) -> str:
        newsession = "".join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))
        )
        if await SessionRepo().get_session_id(db, newsession) is not None:
            await self.__generate_new_session()
        return newsession

    async def create_session(
        self, client_id: str, user: str, ipaddress: str, session_end: datetime
    ) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                newsession = await self.__generate_new_session(db)
                data_create = Session.create(
                    client_id=client_id,
                    session_id=newsession,
                    user=user,
                    session_end=session_end,
                    ipaddress=ipaddress,
                )
                await SessionRepo().save_session(db, data_create)
                return newsession

    async def get_session(self, session_id: int):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await SessionRepo().get_session(db, session_id)

    async def get_session_id(self, session_id: str):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await SessionRepo().get_session_id(db, session_id)

    async def update_session(
        self,
        session_id: int,
        session_update: datetime = None,
        LastPage: str = None,
        Lastipaddress: str = None,
        active: bool = None,
    ) -> bool:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await SessionRepo().get_session(db, session_id)
                if data_get is None:
                    return False
                updates = {}
                if session_update is not None:
                    updates["session_update"] = session_update
                if LastPage is not None:
                    updates["LastPage"] = LastPage
                if Lastipaddress is not None:
                    updates["Lastipaddress"] = Lastipaddress
                if active is not None:
                    updates["active"] = active
                await SessionRepo().update_session(db, data_get, **updates)
                return True

    async def datatable_session(self, params: dict[str, Any]):
        from sqlalchemy import or_, select, case, literal, func
        from core.utils.datatables import DataTable
        from core.db import session_security

        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = select(
                    Session,
                    Session.id.label("DT_RowId"),
                    func.now().label("now"),
                    case(
                        ((Session.session_end >= func.now()) & (Session.active==True), True),
                        else_=False,
                    ).label("active_status"),
                ).order_by(Session.id.desc())
                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=[
                        "DT_RowId",
                        "id",
                        "client_id",
                        "session_id",
                        "user",
                        "session_start",
                        "session_update",
                        "session_end",
                        "Lastipaddress",
                        "LastPage",
                        "now",
                        "active",
                        "active_status",
                    ],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
