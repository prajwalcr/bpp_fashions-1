from flaskapp.models.product import ProductModel
from flaskapp.models.catalog import CatalogModel
from flaskapp.models.category import CategoryModel
from flaskapp.models.size import SizeModel
from flaskapp.models.color import ColorModel
from flaskapp.models.product_category import ProductCategoryModel

from flaskapp.database import Base, engine, SessionLocal

Base.metadata.create_all(engine)

session = SessionLocal()
if session.query(CategoryModel).first() is None:
    root_category = CategoryModel(id=0, level=0)
    session.add(root_category)
    session.commit()
