from app.dao.basedao import BaseDAO
from app.models.users import Users


class UserDAO(BaseDAO):
    model = Users