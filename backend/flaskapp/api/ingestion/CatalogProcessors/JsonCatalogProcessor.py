import json

from flaskapp.api.categories.dal.category import CategoryDAL
from flaskapp.api.products.dal.color import ColorDAL
from flaskapp.api.products.dal.product import ProductDAL
from flaskapp.api.products.dal.product_category import ProductCategoryDAL
from flaskapp.api.products.dal.size import SizeDAL
from flaskapp.api.ingestion.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.database import SessionLocal


class JsonCatalogProcessor(CatalogProcessor):
    """Catalog processor for processing json catalogs."""

    SUPPORTED_EXTENSION = "json"

    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = None

    def load(self) -> bool:
        """
        Load catalog into memory.

        Returns
        -------
        bool
            Returns True if load succeeded, else False.
        """

        try:
            f = open(self.filepath)
        except IOError:
            return False
        try:
            self.data = json.load(f)
        except ValueError:
            return False
        return True

    def validate(self) -> bool:
        """
        Validate uploaded catalog.

        Returns
        -------
        bool
            Returns True if validation succeeded, else False.
        """

        if self.data is None:
            return False

        if type(self.data) != list:
            return False

        for data_item in self.data:
            if type(data_item) != dict:
                return False
            if "uniqueId" not in data_item:
                return False
            if "price" not in data_item:
                return False

        return True

    def ingest(self) -> bool:
        """
        Ingest a valid catalog into database.

        Returns
        -------
        Returns True if ingestion succeeded, else False.
        """

        if self.data is None:
            return False

        # Ingesting all products in a single transaction for consistency.
        with SessionLocal() as session:
            for data_item in self.data:
                id = data_item["uniqueId"]
                title = data_item.get("title", None)
                if "availability" in data_item:
                    availability = data_item["availability"].lower() == "true"
                else:
                    availability = False
                product_description = data_item.get("productDescription", None)
                image_url = data_item.get("productImage", None)
                price = data_item["price"]

                cat_level_names = []
                level_counter = 1
                # Get category level names of the product for each consecutive level starting from 1.
                while True:
                    field = "catlevel"+str(level_counter)+"Name"
                    if field not in data_item:
                        break
                    cat_level_names.append(data_item[field].strip())
                    level_counter += 1

                colors = data_item.get("color", list())
                sizes = data_item.get("size", list())

                category_list = []
                color_list = []
                size_list = []

                # Populating category tree in database
                parent_category = CategoryDAL.find_by_level(session, 0)[0]
                for i in range(len(cat_level_names)):

                    current_category = CategoryDAL.find_if_exists(session, parent_category.id, cat_level_names[i], i+1)

                    if current_category is None:
                        current_category = CategoryDAL.create(parent_category.id, cat_level_names[i], i+1)
                        CategoryDAL.save(session, current_category)
                        session.flush()

                    product_category_association = ProductCategoryDAL.create(id, current_category.id)

                    category_list.append(product_category_association)

                    # Current category becomes parent category for its lower level categories.
                    parent_category = current_category

                for color in colors:
                    color_list.append(ColorDAL.create(id, color))

                for size in sizes:
                    size_list.append(SizeDAL.create(id, size))

                product = ProductDAL.create(
                    id=id,
                    title=title,
                    availability=availability,
                    product_description=product_description,
                    image_url=image_url,
                    price=price,
                    product_category_associations=category_list,
                    colors=color_list,
                    sizes=size_list
                )

                ProductDAL.save(session, product)
                # time.sleep(0.02)
            try:
                session.commit()
            except Exception as error:
                print("Exception in ingestion", error)
                session.flush()
                session.rollback()
                return False

        return True
