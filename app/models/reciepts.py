from datetime import date, datetime

from sqlalchemy import ForeignKey, Date, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Receipts(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Уникальный идентификатор чека
    total_amount: Mapped[int]  # Общая сумма чека
    received_amount: Mapped[int | None]  # Сумма, полученная от покупателя
    change: Mapped[int | None]  # Сдача
    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) # Время создания чека
    user_id = mapped_column(ForeignKey("users.id", ondelete="SET NULL")) # кто продал




    products: Mapped[list["Products"]] = relationship(back_populates="receipts",
                                                      secondary="receipt_items",
                                                      lazy='joined')
    user: Mapped["Users"] = relationship(back_populates="receipts", lazy='joined')
    receipt_to_products: Mapped["ReceiptItems"] = relationship(back_populates="receipts", viewonly=True)


class ReceiptItems(Base):
    __tablename__ = "receipt_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Уникальный идентификатор позиции
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))  # Ссылка на чек
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))# Ссылка на продукт
    quantity: Mapped[int]  # Количество продукта
    price: Mapped[int] #стоимость

    # # Связи между таблицами
    receipts: Mapped["Receipts"] = relationship(back_populates="receipt_to_products", overlaps="products, receipts")
    products: Mapped["Products"] = relationship(back_populates="products_to_receipts", overlaps="products, receipts")
