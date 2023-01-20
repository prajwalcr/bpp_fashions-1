# from flaskapp import db

from flaskapp import Base
from sqlalchemy import Column, String, Boolean, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(String(50), primary_key=True)
    status = Column(String(50))
    filepath = Column(String(200), nullable=False)

    def __repr__(self):
        return f"Catalog('{self.id}, '{self.status}')"
# from flaskapp import db


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {'extend_existing':True}
    id = Column(String(15), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)
    category = relationship("Category", backref="product", uselist=False, lazy=True)
    size = relationship("Size", backref="product", lazy=True, uselist=False)
    colour = relationship("Colour", backref="product", lazy=True, uselist=False)

    def __repr__(self):
        return f"Product('{self.id}', f'{self.price}')"


class Category(Base):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    id = Column(String(15), primary_key=True)
    product_id = Column(String(15), ForeignKey("product.id"), nullable=False)
    # product = relationship("Product", backref="category", uselist=False, lazy=True)
    category_name = Column(String(40))
    parent_category = Column(String(40))



class Size(Base):
    __tablename__ = "size"
    __table_args__ = {'extend_existing': True}

    id = Column(String(15), primary_key=True)
    product_size = Column(Text, primary_key=True)
    product_id = Column(String(15), ForeignKey("product.id"), nullable=False)
    #product = relationship("Product", back_populates="size")


class Colour(Base):
    __tablename__ = "colour"
    __table_args__ = {'extend_existing': True}
    id = Column(String(15), primary_key=True)
    product_colour = Column(Text, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    #product = relationship("Product", back_populates="colour")

#
# class Gender(Model):
#     __tablename__ = "gender"
#     __table_args__ = {'extend_existing': True}
#     id = Column(String(15), primary_key=True)
#     product_gender = Column(Enum('male', 'female', 'other', name='varchar'))
#




