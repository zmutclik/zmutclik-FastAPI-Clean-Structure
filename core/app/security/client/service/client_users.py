from datetime import datetime, timezone

from ..domain import ClientUser
from ..exceptions import ClientNotFoundException
from ..repository import ClientRepo, ClientUserRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class ClientUserService:
    async def add_clientuser(self, client_id: int, user: str) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientUserRepo().get_clientuser(db, client_id, user)
                if data_get is None:
                    data_create = ClientUser().create(client_id=client_id, user=user)
                    await ClientUserRepo().save_clientuser(db, data_create)
                else:
                    await ClientUserRepo().update_clientuser(db, data_get, LastLogin=datetime.now(timezone.utc))

    async def get_clientuser(self, client_id: int, user: str) -> ClientUser:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientUserRepo().get_clientuser(db, client_id, user)

    async def get_clientusers(self, client_id: str):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_client = await ClientRepo().get_client_id(db, client_id)
                if data_client is None:
                    return None
                return await ClientUserRepo().get_clientusers(db, data_client.id)

    async def update_clientuser(self, client_id: int, user: str, LastPage: str = None, Lastipaddress: str = None):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientUserRepo().get_clientuser(db, client_id, user)
                if data_get is None:
                    return False
                updates = {"LastLogin": datetime.now(timezone.utc)}
                if LastPage is not None:
                    updates["LastPage"] = LastPage
                if Lastipaddress is not None:
                    updates["Lastipaddress"] = Lastipaddress

                await ClientUserRepo().update_clientuser(db, data_get, **updates)
