from typing import Union, Optional, Any
from pythondi import inject
import random
import string
from datetime import datetime
from fastapi import Request
from user_agents import parse

from ..domain import Client, ClientUser
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

    async def add_user(self, client_id: str, user: str) -> bool:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_client = await ClientRepo().get_client_id(db, client_id)
                if data_client is None:
                    return False
                data_get = await ClientUserRepo().get_clientuser(db, data_client.id, user)
                if data_get is None:
                    data_create = ClientUser().create(client_id=data_client.id, user=user)
                    await ClientUserRepo().save_clientuser(db, data_create)
                    return True
                else:
                    await ClientUserRepo().update_clientuser(db, data_get, LastLogin=datetime.now())
                    return True

    async def get_client_id(self, client_id: str):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientRepo().get_client_id(db, client_id)

    async def update_clientuser(
        self,
        client_id: int,
        user: str,
        LastLogin: datetime = None,
        LastPage: str = None,
    ) -> bool:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientUserRepo().get_clientuser(db, client_id, user)
                if data_get is None:
                    return False
                updates = {}
                if LastLogin is not None:
                    updates["LastLogin"] = LastLogin
                if LastPage is not None:
                    updates["LastPage"] = LastPage
                await ClientUserRepo().update_clientuser(db, data_get, **updates)
                return True

    async def datatable_client(self, params: dict[str, Any]):
        from sqlalchemy import or_, select
        from core.utils.datatables import DataTable
        from core.db import session_security

        query = select(Client, Client.client_id.label("DT_RowId"))
        datatable: DataTable = DataTable(
            request_params=params,
            table=query,
            column_names=["DT_RowId", "id", "client_id", "platform", "browser"],
            engine=session_security,
            # callbacks=callbacks,
        )
        await datatable.generate()
        return datatable.output_result()
