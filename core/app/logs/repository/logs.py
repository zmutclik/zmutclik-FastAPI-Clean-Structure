from uuid import uuid4
from typing import Optional, List, Union
from datetime import datetime
import time
from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, func, distinct
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Logs, IpAddress, RouterName, UserName, ClientID
from core.exceptions import DatabaseSavingException

from core.db.session_logs import async_engine


class LogsRepo:
    async def get_ipaddress(self, tahunbulan: datetime = None):
        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                result = await db.execute(
                    select(IpAddress.ipaddress, func.count(IpAddress.id).label("count"))
                    .group_by(IpAddress.ipaddress)
                    .order_by(func.count(IpAddress.id).desc())
                )
                return result.all()

    async def get_routers_name(self, tahunbulan: datetime = None):
        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                result = await db.execute(
                    select(RouterName.routername, func.count(RouterName.id).label("count"))
                    .group_by(RouterName.routername)
                    .order_by(RouterName.routername)
                )
                return result.all()

    async def get_username(self, tahunbulan: datetime = None):
        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                result = await db.execute(
                    select(UserName.username, func.count(UserName.id).label("count")).group_by(UserName.username).order_by(UserName.username)
                )
                return result.all()

    async def get_clientid(self, tahunbulan: datetime = None):
        async with async_engine(tahunbulan).begin() as connection:
            async with AsyncSession(bind=connection) as db:
                result = await db.execute(
                    text("""
                        SELECT clientid, platform, browser, 
                               GROUP_CONCAT(DISTINCT username) AS usernames, 
                               COUNT(id) AS count
                        FROM logs_clientid
                        GROUP BY clientid, platform, browser
                        ORDER BY count DESC
                    """)
                )
                
                return [
                    {
                        "clientid": row[0],
                        "platform": row[1],
                        "browser": row[2],
                        "usernames": row[3],  # Usernames akan dipisahkan dengan koma otomatis di SQLite
                        "count": row[4]
                    }
                    for row in result.fetchall()
                ]

    async def save(self, logs: Logs):
        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                try:
                    db.add(logs)
                    db.add(IpAddress(ipaddress=logs.ipaddress))
                    db.add(RouterName(routername=logs.router))
                    db.add(UserName(username=logs.user))
                    db.add(ClientID(clientid=logs.client_id, username=logs.user, platform=logs.platform, browser=logs.browser))
                    await db.commit()
                except SQLAlchemyError as e:
                    raise DatabaseSavingException(f"Error saving logs: {str(e)}")
