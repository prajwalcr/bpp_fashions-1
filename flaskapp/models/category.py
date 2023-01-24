from flaskapp.database import Base
from sqlalchemy import Column, String, ForeignKey

class CategoryModel(Base):
    __tablename__ = "category"
    # __table_args__ = {'extend_existing': True}

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    catlevel1 = Column(String(40))
    catlevel2 = Column(String(40))

    def __repr__(self):
        return f"Category('{self.product_id}', '{self.catlevel1}', '{self.catlevel2}')"
