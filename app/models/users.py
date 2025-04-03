from typing import Optional

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True) #уникальный инд
    name: Mapped[str] #имя пользователя
    email: Mapped[str]
    # hashed_password: Mapped[bytes] = mapped_column(LargeBinary)
    hashed_password: Mapped[str]
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey('roles.id')) #роль

    role = relationship('Roles', back_populates='user')

    def __repr__(self) -> str:
        return f"User( name={self.name!r})"

class Roles(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True) # уникальный инд
    role_name: Mapped[str]  #роль в системе(продавец, владелец)

    user = relationship('Users', back_populates='role')
