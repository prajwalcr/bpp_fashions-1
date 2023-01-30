from flaskapp.database import Base
from sqlalchemy import Column, String, Boolean, Text, Float
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__ = "product"
    # __table_args__ = {'extend_existing':True}

    id = Column(String(15), primary_key=True)
    title = Column(String(80))
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)
    category = relationship("CategoryModel", backref="product", uselist=False, lazy=True)
    sizes = relationship("SizeModel", backref="product", lazy=True)
    colors = relationship("ColorModel", backref="product", lazy=True)

    def __repr__(self):
        return f"Product('{self.id}', '{self.title}, '{self.price}')"
