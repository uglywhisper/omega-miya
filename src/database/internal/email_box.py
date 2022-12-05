"""
@Author         : Ailitonia
@Date           : 2022/12/04 16:11
@FileName       : email_box.py
@Project        : nonebot2_miya 
@Description    : EmailBox DAL
@GitHub         : https://github.com/Ailitonia
@Software       : PyCharm 
"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import Optional

from pydantic import BaseModel, parse_obj_as

from ..model import BaseDataAccessLayerModel, EmailBoxOrm


class EmailBox(BaseModel):
    """邮箱 Model"""
    id: int
    address: str
    server_host: str
    protocol: str
    port: int
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = 'ignore'
        orm_mode = True
        allow_mutation = False


class EmailBoxDAL(BaseDataAccessLayerModel):
    """邮箱 数据库操作对象"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def query_unique(self, address: str) -> EmailBox:
        stmt = select(EmailBoxOrm).where(EmailBoxOrm.address == address)
        session_result = await self.db_session.execute(stmt)
        return EmailBox.from_orm(session_result.scalar_one())

    async def query_all(self) -> list[EmailBox]:
        stmt = select(EmailBoxOrm).order_by(EmailBoxOrm.address)
        session_result = await self.db_session.execute(stmt)
        return parse_obj_as(list[EmailBox], session_result.scalars().all())

    async def add(self, address: str, server_host: str, protocol: str, port: int, password: str) -> None:
        new_obj = EmailBoxOrm(address=address, server_host=server_host, protocol=protocol, port=port,
                              password=password, created_at=datetime.now())
        self.db_session.add(new_obj)
        await self.db_session.flush()

    async def update(
            self,
            id_: int,
            *,
            address: Optional[str] = None,
            server_host: Optional[str] = None,
            protocol: Optional[str] = None,
            port: Optional[int] = None,
            password: Optional[str] = None
    ) -> None:
        stmt = update(EmailBoxOrm).where(EmailBoxOrm.id == id_)
        if address is not None:
            stmt = stmt.values(address=address)
        if server_host is not None:
            stmt = stmt.values(server_host=server_host)
        if protocol is not None:
            stmt = stmt.values(protocol=protocol)
        if port is not None:
            stmt = stmt.values(port=port)
        if password is not None:
            stmt = stmt.values(password=password)
        stmt = stmt.values(updated_at=datetime.now())
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def delete(self, id_: int) -> None:
        stmt = delete(EmailBoxOrm).where(EmailBoxOrm.id == id_)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)


__all__ = [
    'EmailBox',
    'EmailBoxDAL'
]
