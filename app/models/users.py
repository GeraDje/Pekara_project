from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    hashed_password: Mapped[str]

    def __repr__(self) -> str:
        return f"User( name={self.name!r})"