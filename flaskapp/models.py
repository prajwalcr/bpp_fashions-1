# from flaskapp import db

from flaskapp import Base
from sqlalchemy import Column, String, Boolean, Text, Float

class Product(Base):
    __tablename__ = "product"

    id = Column(String(15), primary_key=True)
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)

    def __repr__(self):
        return f"Product('{self.id}, '{self.price}')"


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(String(50), primary_key=True)
    status = Column(String(50))
    filepath = Column(String(200), nullable=False)

    def __repr__(self):
        return f"Catalog('{self.id}, '{self.status}')"



