from flaskapp.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

# ProductCategoryModel = Table(
#     "product_category",
#     Base.metadata,
#     Column("product_id", String(15), ForeignKey("product.id"), primary_key=True),
#     Column("category_id", Integer, ForeignKey("category.id"), primary_key=True)
# )

class ProductCategoryModel(Base):
    __tablename__ = "product_category"
    # __table_args__ = {'extend_existing':True}

    product_id = Column(String(15), ForeignKey("product.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    category = relationship("CategoryModel", backref="product_category", uselist=False)

    def __repr__(self):
        return f"Product_Category('{self.product_id}', '{self.category_id})"
