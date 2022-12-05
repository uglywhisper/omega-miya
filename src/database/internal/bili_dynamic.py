"""
@Author         : Ailitonia
@Date           : 2022/12/04 21:29
@FileName       : bili_dynamic.py
@Project        : nonebot2_miya 
@Description    : BiliDynamic DAL
@GitHub         : https://github.com/Ailitonia
@Software       : PyCharm 
"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, desc
from typing import Optional

from pydantic import BaseModel, parse_obj_as

from ..model import BaseDataAccessLayerModel, BiliDynamicOrm


class BiliDynamic(BaseModel):
    """B站动态 Model"""
    id: int
    dynamic_id: int
    dynamic_type: int
    uid: int
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = 'ignore'
        orm_mode = True
        allow_mutation = False


class BiliDynamicDAL(BaseDataAccessLayerModel):
    """B站动态 数据库操作对象"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def query_unique(self, dynamic_id: int) -> BiliDynamic:
        stmt = select(BiliDynamicOrm).where(BiliDynamicOrm.dynamic_id == dynamic_id)
        session_result = await self.db_session.execute(stmt)
        return BiliDynamic.from_orm(session_result.scalar_one())

    async def query_user_all(self, uid: int) -> list[BiliDynamic]:
        """查询用户的全部动态"""
        stmt = select(BiliDynamicOrm).where(BiliDynamicOrm.uid == uid).order_by(desc(BiliDynamicOrm.dynamic_id))
        session_result = await self.db_session.execute(stmt)
        return parse_obj_as(list[BiliDynamic], session_result.scalars().all())

    async def query_user_all_dynamic_ids(self, uid: int) -> list[int]:
        """查询用户的全部动态id"""
        stmt = select(BiliDynamicOrm.dynamic_id).\
            where(BiliDynamicOrm.uid == uid).\
            order_by(desc(BiliDynamicOrm.dynamic_id))
        session_result = await self.db_session.execute(stmt)
        return parse_obj_as(list[int], session_result.scalars().all())

    async def query_all(self) -> list[BiliDynamic]:
        stmt = select(BiliDynamicOrm).order_by(desc(BiliDynamicOrm.dynamic_id))
        session_result = await self.db_session.execute(stmt)
        return parse_obj_as(list[BiliDynamic], session_result.scalars().all())

    async def add(self, dynamic_id: int, dynamic_type: int, uid: int, content: str) -> None:
        new_obj = BiliDynamicOrm(dynamic_id=dynamic_id, dynamic_type=dynamic_type,
                                 uid=uid, content=content, created_at=datetime.now())
        self.db_session.add(new_obj)
        await self.db_session.flush()

    async def update(
            self,
            id_: int,
            *,
            dynamic_id: Optional[int] = None,
            dynamic_type: Optional[int] = None,
            uid: Optional[int] = None,
            content: Optional[str] = None
    ) -> None:
        stmt = update(BiliDynamicOrm).where(BiliDynamicOrm.id == id_)
        if dynamic_id is not None:
            stmt = stmt.values(dynamic_id=dynamic_id)
        if dynamic_type is not None:
            stmt = stmt.values(dynamic_type=dynamic_type)
        if uid is not None:
            stmt = stmt.values(uid=uid)
        if content is not None:
            stmt = stmt.values(content=content)
        stmt = stmt.values(updated_at=datetime.now())
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def delete(self, id_: int) -> None:
        stmt = delete(BiliDynamicOrm).where(BiliDynamicOrm.id == id_)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)


__all__ = [
    'BiliDynamic',
    'BiliDynamicDAL'
]
