# from flaskapp import db

from flaskapp import Base
from sqlalchemy import Column, String, Boolean, Text, Float, ForeignKey
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
    title = Column(String(80))
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)
    category = relationship("Category", backref="product", uselist=False, lazy=True)
    sizes = relationship("Size", backref="product", lazy=True)
    colors = relationship("Color", backref="product", lazy=True)

    def __repr__(self):
        return f"Product('{self.id}', f'{self.price}')"


class Category(Base):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    # product = relationship("Product", backref="category", uselist=False, lazy=True)
    catlevel2 = Column(String(40))
    catlevel1 = Column(String(40))



class Size(Base):
    __tablename__ = "size"
    __table_args__ = {'extend_existing': True}

    product_size = Column(Text, primary_key=True)
    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    #product = relationship("Product", back_populates="size")


class Color(Base):
    __tablename__ = "color"
    __table_args__ = {'extend_existing': True}
    product_color = Column(Text, primary_key=True)
    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    #product = relationship("Product", back_populates="color")

#
# class Gender(Model):
#     __tablename__ = "gender"
#     __table_args__ = {'extend_existing': True}
#     id = Column(String(15), primary_key=True)
#     product_gender = Column(Enum('male', 'female', 'other', name='varchar'))
#




