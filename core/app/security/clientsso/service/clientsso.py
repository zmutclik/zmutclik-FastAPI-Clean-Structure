from typing import Union, Optional, Any
from pythondi import inject
import random, string

from ..domain import ClientSSO, ClientSSO_code
from ..repository import ClientSSORepo, ClientSSOCodeRepo
from ..schema import ClientSSOSchema, ClientSSOCodeSchema
from ..exceptions import ClientSSONotFoundException, ClientSSODuplicateException
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class ClientSSOService:
    async def get_clientsso(self, clientsso_id: str) -> Optional[ClientSSOSchema]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientSSORepo().get_clientsso(db, clientsso_id)

    async def get_clientsso_code(self, clientsso_id: str, code: str) -> Optional[ClientSSOCodeSchema]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientSSOCodeRepo().get_clientsso_code(db, clientsso_id, code)

    async def get_clientsso_findcode(self, code: str) -> Optional[ClientSSOCodeSchema]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientSSOCodeRepo().get_clientsso_findcode(db, code)

    async def check_clientsso(self, db: AsyncSession) -> str:
        clientsso_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        clientssocode = await ClientSSORepo().get_clientsso(db, clientsso_id)
        if clientssocode is None:
            return clientsso_id
        return await self.check_clientsso(db)

    async def create_clientsso(self, created_user: str, nama: str, ipaddress: str, callback_uri: str) -> ClientSSOSchema:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_create = ClientSSO.create(
                    created_user=created_user,
                    clientsso_id=await self.check_clientsso(db),
                    nama=nama,
                    ipaddress=ipaddress,
                    callback_uri=callback_uri,
                )
                data_saved = await ClientSSORepo().save_clientsso(db, clientsso=data_create)
                return data_saved

    async def check_clientsso_code(self, db: AsyncSession, clientsso_id: str) -> str:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(4, 8)))
        clientssocode = await ClientSSOCodeRepo().get_clientsso_code(db, clientsso_id, code)
        if clientssocode is None:
            return code
        return await self.check_clientsso_code(db, clientsso_id)

    async def create_clientsso_code(self, clientsso_id: str, user_id: int, client_id: str) -> ClientSSOSchema:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_create = ClientSSO_code.create(
                    clientsso_id=clientsso_id,
                    client_id=client_id,
                    code=await self.check_clientsso_code(db, clientsso_id),
                    user_id=user_id,
                )
                data_saved = await ClientSSOCodeRepo().save_clientsso_code(db, clientsso_code=data_create)
                return data_saved

    async def update_clientsso(
        self,
        clientsso_id: str,
        clientsso_secret: Union[bool, None] = None,
        nama: Union[str, None] = None,
        ipaddress: Union[str, None] = None,
        callback_uri: Union[str, None] = None,
        disabled: Union[bool, None] = None,
    ) -> ClientSSOSchema:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientSSORepo().get_clientsso(db, clientsso_id)
                if not data_get:
                    raise ClientSSONotFoundException

                updates = {}
                if clientsso_secret is not None and clientsso_secret:
                    updates["clientsso_secret"] = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
                if nama is not None:
                    updates["nama"] = nama
                if ipaddress is not None:
                    updates["ipaddress"] = ipaddress
                if disabled is not None:
                    updates["disabled"] = disabled
                if callback_uri is not None:
                    updates["callback_uri"] = callback_uri

                return await ClientSSORepo().update_clientsso(db, data_get, **updates)

    async def delete_clientsso(self, clientsso_id: str, username: str) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await ClientSSORepo().get_clientsso(db, clientsso_id)
                if not data_get:
                    raise ClientSSONotFoundException

                await ClientSSORepo().delete_clientsso(db, data_get, username)

    async def delete_clientsso_code(self, client_id: str) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                await ClientSSOCodeRepo().delete_clientsso_code(db, client_id)

    async def datatable_clientsso(self, params: dict[str, Any]):
        from sqlalchemy import or_, select, func
        from core.utils.datatables import DataTable

        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = (
                    select(ClientSSO, ClientSSO.clientsso_id.label("DT_RowId")).filter(ClientSSO.deleted_at == None).order_by(ClientSSO.nama.desc())
                )

                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=["DT_RowId", "clientsso_id", "nama", "ipaddress", "disabled", "created_at", "created_user"],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
