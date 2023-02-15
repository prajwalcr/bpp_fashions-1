from flaskapp.models.product import ProductModel
from flaskapp.models.catalog import CatalogModel
from flaskapp.models.category import CategoryModel
from flaskapp.models.size import SizeModel
from flaskapp.models.color import ColorModel
from flaskapp.models.product_category import ProductCategoryModel

from flaskapp.database import Base, engine, SessionLocal

# Create all the SQL tables in database if they don't exist
Base.metadata.create_all(engine)

session = SessionLocal()

# Add category level 0 item into the database on startup if it does not already exist.
# This category behaves as the parent of all other categories.
if session.query(CategoryModel).first() is None:
    root_category = CategoryModel(id=0, level=0)
    session.add(root_category)
    session.commit()
