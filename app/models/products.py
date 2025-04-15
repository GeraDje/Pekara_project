from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base



class Products(Base):
    __tablename__ = 'products'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]
    price:Mapped[int]

    def __repr__(self) -> str:
        return f"Product({self.name}, {self.price})"

    products_to_receipts: Mapped["ReceiptItems"] = relationship(
        back_populates="products",
        overlaps="receipts, products"
    )
