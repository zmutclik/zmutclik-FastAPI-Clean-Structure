from typing import Optional, Any
from datetime import datetime, timezone

from ..domain import ClientUserOtp, Client
from ..repository import ClientRepo, ClientUserRepo, ClientUserOTPRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class ClientUserOTPService:
    async def get_clientusers_otp(self, client_id: str, user: str) -> Optional[ClientUserOtp]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_client = await ClientRepo().get_client_id(db, client_id)
                if data_client is None:
                    return None
                data_client_user = await ClientUserRepo().get_clientuser(db, data_client.id, user)
                if data_client_user is None:
                    return None
                return await ClientUserOTPRepo().get_clientuser_otp(db, data_client.id, user)

    async def create_clientuser(self, client_id: str, user: str, session_end: datetime) -> Optional[ClientUserOtp]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_client = await ClientRepo().get_client_id(db, client_id)
                if data_client is None:
                    return None
                data_create = ClientUserOtp.create(client_id=data_client.id, user=user, session_end=session_end)
                data_saved = await ClientUserOTPRepo().save_clientuser_otp(db, clientuserotp=data_create)
                return data_saved

    async def delete_clientusers_otp(self, data_client_id: int, user) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_otp = await ClientUserOTPRepo().get_clientuser_otp(db, data_client_id, user)
                await ClientUserOTPRepo().update_clientuser_otp(db, data_otp, active=False)

    async def datatable_clientotp(self, params: dict[str, Any]):
        from sqlalchemy import or_, select, func, case
        from core.utils.datatables import DataTable

        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                query = (
                    select(
                        ClientUserOtp,
                        ClientUserOtp.id.label("DT_RowId"),
                        Client.client_id.label("client_id_str"),
                        case(
                            ((ClientUserOtp.session_end >= func.now()) & (ClientUserOtp.active == True), True),
                            else_=False,
                        ).label("active_status"),
                    )
                    .join(ClientUserOtp.CLIENT)
                    .order_by(ClientUserOtp.session_start.desc())
                )
                datatable: DataTable = DataTable(
                    request_params=params,
                    table=query,
                    column_names=["DT_RowId", "id", "client_id_str", "user", "otp", "session_start", "session_end", "active_status"],
                    engine=db,
                    # callbacks=callbacks,
                )
                await datatable.generate()
                return datatable.output_result()
