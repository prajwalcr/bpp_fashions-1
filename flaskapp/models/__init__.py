from flaskapp.models.product import ProductModel
from flaskapp.models.catalog import CatalogModel
from flaskapp.models.category import CategoryModel
from flaskapp.models.size import SizeModel
from flaskapp.models.color import ColorModel

from flaskapp.database import Base, engine

Base.metadata.create_all(engine)
