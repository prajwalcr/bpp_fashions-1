from flaskapp.database import Base
from sqlalchemy import Column, String, Text, ForeignKey


class ColorModel(Base):
    __tablename__ = "color"
    # __table_args__ = {'extend_existing': True}

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    product_color = Column(Text, primary_key=True)

    def __repr__(self):
        return f"Color('{self.product_id}', '{self.product_color}')"
