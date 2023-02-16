from flaskapp.database import Base
from sqlalchemy import Column, String, Text, ForeignKey


class SizeModel(Base):
    """ORM class for size objects."""
    __tablename__ = "size"

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    product_size = Column(Text, primary_key=True)

    def __repr__(self):
        """Returns a readable representation of a size object."""
        return f"Size('{self.product_id}', '{self.product_size}')"
