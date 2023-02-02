from flaskapp.database import Base
from sqlalchemy import Column, String, Boolean, Text, Float
from sqlalchemy.orm import relationship
from flaskapp.models.product_category import ProductCategoryModel


class ProductModel(Base):
    __tablename__ = "product"
    # __table_args__ = {'extend_existing':True}

    id = Column(String(15), primary_key=True)
    title = Column(String(80))
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)
    categories = relationship("ProductCategoryModel", backref="product", uselist=True)
    # deepest_category_id = Column(Integer, ForeignKey("category.id"))
    # category = relationship("CategoryModel", backref="product", uselist=False, lazy=True)
    sizes = relationship("SizeModel", backref="product", lazy=True)
    colors = relationship("ColorModel", backref="product", lazy=True)

    def __repr__(self):
        return f"Product('{self.id}', '{self.title}, '{self.price}')"

    @classmethod
    def find_by_id_query(cls, db, id):
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db):
        return db.query(cls)

    @classmethod
    def find_by_category_id_query(cls, db, category_id):
        return db.query(cls) \
            .join(ProductCategoryModel) \
            .filter(ProductCategoryModel.category_id == category_id)

    @classmethod
    def order_by_price_query(cls, q, reverse=False):
        if reverse:
            return q.order_by(cls.price.desc())
        return q.order_by(cls.price)

    @classmethod
    def paginate_query(cls, q, rows, page):
        return q.limit(rows).offset((page - 1) * rows)

    @classmethod
    def count(cls, q):
        return q.count()

    @classmethod
    def find_by_id(cls, db, id):
        return cls.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db):
        return cls.find_all_query(db).all()

    @classmethod
    def find_by_category_id(cls, db, category_id):
        return cls.find_by_category_id_query(db, category_id)

    @classmethod
    def order_by_price(cls, q, reverse=False):
        return cls.order_by_price_query(q, reverse).all()

    @classmethod
    def paginate(cls, q, rows, page):
        return cls.paginate_query(q, rows, page).all()

    def save(self, db):
        db.add(self)
