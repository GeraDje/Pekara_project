from mako.compat import win32
from sqlalchemy import insert,text, select,func
import asyncio
from app.dao.basedao import BaseDAO
from app.database import async_session_maker
from app.models.reciepts import ReceiptItems, Receipts
from datetime import datetime, timedelta

class ReceiptItemDAO(BaseDAO):
    model = ReceiptItems

class ReceiptsDAO(BaseDAO):

    model=Receipts

    @classmethod
    async def get_max_id(cls):
        async with async_session_maker() as session:
            try:
                sql_query = text(f"SELECT Max(receipts.id) from receipts")
                result = await session.execute(sql_query)
                row = result.fetchone()
                if row:
                    max_id = row[0]
                    return max_id
                else:
                    return None
            except Exception as e:
                print(f"Ошибка при получении максимального ID: {e}")
                return None


    @classmethod
    async def get_sum_to_week(cls):
        async with async_session_maker() as session:
            try:
                sql_query = text(f""
                                 f"SELECT sum(receipts.total_amount) "
                                 f"from receipts "
                                 f"WHERE receipts.created_at >= DATE_TRUNC('week', CURRENT_DATE)" 
                                 f"AND receipts.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'")
                result = await session.execute(sql_query)
                return result.scalar()
            except Exception as e:
                print(f"Ошибка при получении суммы за неделю: {e}")
                return None



    @classmethod
    async def get_sum_today(cls) -> float:
        async with async_session_maker() as session:
            try:
                sql_query = text(f""
                                 f"SELECT sum(receipts.total_amount) "
                                 f"from receipts "
                                 f"WHERE receipts.created_at::date = CURRENT_DATE")
                result = await session.execute(sql_query)
                return result.scalar()
            except Exception as e:
                print(f"Ошибка при получении суммы за неделю: {e}")
                return None


    @classmethod
    async def get_sum_mounth(cls) -> float:
        async with async_session_maker() as session:
            try:
                sql_query = text("""SELECT SUM(receipts.total_amount) 
                                    FROM receipts 
                                    WHERE receipts.created_at >= date_trunc('month', CURRENT_DATE)
                                    AND receipts.created_at < date_trunc('month', CURRENT_DATE) + interval '1 month'""")
                result = await session.execute(sql_query)
                return result.scalar()
            except Exception as e:
                print(f"Ошибка при получении суммы за месяц: {e}")
                return None
