from flaskapp.database import Base
from sqlalchemy import Column, String, Text, ForeignKey


class SizeModel(Base):
    __tablename__ = "size"
    # __table_args__ = {'extend_existing': True}

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    product_size = Column(Text, primary_key=True)

    def __repr__(self):
        return f"Size('{self.product_id}', '{self.product_size}')"
