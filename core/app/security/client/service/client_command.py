from typing import Union, Optional, Any
from pythondi import inject
import random
import string
from datetime import datetime, timezone
from fastapi import Request
from user_agents import parse

from ..domain import Client, ClientUser
from ..exceptions import ClientNotFoundException
from ..repository import ClientRepo, ClientUserRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class ClientService:
    async def __generate_new_client(self, db: AsyncSession) -> str:
        newclient = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
        if await ClientRepo().get_client_id(db, newclient) is not None:
            await self.__generate_new_client()
        return newclient

    async def new_client(self, request: Request) -> str:
        try:
            user_agent = parse(request.headers.get("user-agent"))
            platform = user_agent.os.family + user_agent.os.version_string
            browser = user_agent.browser.family + user_agent.browser.version_string
        except:
            platform = ""
            browser = ""
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                newclient = await self.__generate_new_client(db)
                data_create = Client.create(client_id=newclient, platform=platform, browser=browser)
                await ClientRepo().save_client(db, data_create)
                return newclient

    async def get_client_id(self, client_id: str):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientRepo().get_client_id(db, client_id)

    async def update_client(self, client_id: int, disabled: bool = None):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientRepo().get_client(db, client_id)
                if data_get is None:
                    raise ClientNotFoundException
                updates = {}
                if disabled is not None:
                    updates["disabled"] = disabled
                await ClientRepo().update_client(db, data_get, **updates)

    async def datatable_client(self, params: dict[str, Any]):
        from sqlalchemy import or_, select, func
        from core.utils.datatables import DataTable

        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = (
                    select(
                        Client,
                        Client.client_id.label("DT_RowId"),
                        func.max(ClientUser.LastLogin).label("LastLogin"),
                        func.group_concat(ClientUser.user, ", ").label("users"),
                    )
                    .join(Client.USERS)
                    .group_by(Client.id)
                    .order_by(func.max(ClientUser.LastLogin).desc())
                )
                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=["DT_RowId", "id", "client_id", "platform", "browser", "users", "LastLogin", "disabled"],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
