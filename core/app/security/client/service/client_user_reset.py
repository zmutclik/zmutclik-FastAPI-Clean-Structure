from typing import Optional, Any
from datetime import datetime, timezone
import random, string

from ..domain import ClientUserResetCode
from ..repository import ClientUserResetCodeRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class ClientUserResetService:
    async def __generate_new_code(self, db: AsyncSession, user: str) -> str:
        newcode = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        if await ClientUserResetCodeRepo().get_clientuser_reset_code(db, user, newcode) is not None:
            await self.__generate_new_code()
        return newcode

    async def __generate_new_salt(self, db: AsyncSession, user: str) -> str:
        newcode = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        if await ClientUserResetCodeRepo().get_clientuser_reset_code(db, user, newcode) is not None:
            await self.__generate_new_salt()
        return newcode

    async def get_clientusers_reset(self, user: str) -> Optional[ClientUserResetCode]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientUserResetCodeRepo().get_clientuser_reset(db, user)

    async def get_clientusers_reset_by_salt(self, salt: str) -> Optional[ClientUserResetCode]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                return await ClientUserResetCodeRepo().get_clientuser_reset_by_salt(db, salt)

    async def create_clientuser_reset(self, user: str) -> Optional[ClientUserResetCode]:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_client = await ClientUserResetCodeRepo().get_clientuser_reset(db, user)
                if data_client is not None:
                    return False
                newcode = await self.__generate_new_code(db, user)
                newsalt = await self.__generate_new_salt(db, user)
                data_create = ClientUserResetCode.create(user=user, code=newcode, salt=newsalt)
                data_saved = await ClientUserResetCodeRepo().save_clientuser_reset(db, data_create)
                return data_saved

    async def delete_clientusers_reset(self, user: str) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_otp = await ClientUserResetCodeRepo().get_clientuser_reset(db, user)
                await ClientUserResetCodeRepo().update_clientuser_reset(db, data_otp, active=False)
