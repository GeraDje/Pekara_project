from app.dao.basedao import BaseDAO
from app.models.products import Products


class ProductsDAO(BaseDAO):
    model=Products