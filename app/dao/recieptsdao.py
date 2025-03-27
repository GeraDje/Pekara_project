from sqlalchemy import insert,text

from app.dao.basedao import BaseDAO
from app.database import async_session_maker
from app.models.reciepts import ReceiptItems, Receipts


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