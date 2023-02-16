from flaskapp.database import Base
from sqlalchemy import Column, String, Text, ForeignKey


class ColorModel(Base):
    """ORM class for color objects."""
    __tablename__ = "color"

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    product_color = Column(Text, primary_key=True)

    def __repr__(self):
        """Returns a readable representation of a color object."""
        return f"Color('{self.product_id}', '{self.product_color}')"
