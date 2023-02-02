import json
from flaskapp.models import ProductModel, CategoryModel, ColorModel, SizeModel, ProductCategoryModel
from flaskapp.api.ingestion.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.database import SessionLocal


class JsonCatalogProcessor(CatalogProcessor):

    SUPPORTED_EXTENSION = "json"

    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = None

    def load(self):
        try:
            f = open(self.filepath)
        except IOError:
            return False
        try:
            self.data = json.load(f)
        except ValueError:
            return False
        return True

    def validate(self):
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

    def ingest(self):
        if self.data is None:
            return False

        # Session = db.sessionmaker()
        with SessionLocal() as session:
            for data_item in self.data:
                id = data_item["uniqueId"]
                title = data_item.get("title", None)
                if "availability" in data_item:
                    availability = data_item["availability"].lower() == "true"
                else:
                    availability = False
                product_description = data_item.get("productDescription", None)
                image_url = data_item.get("productImage", None)  # Replace this maybe
                price = data_item["price"]

                cat_level_names = []
                level_counter = 1
                while True:
                    field = "catlevel"+str(level_counter)+"Name"
                    if field not in data_item:
                        break
                    cat_level_names.append(data_item[field].strip())
                    level_counter += 1

                colors = data_item.get("color", list())
                sizes = data_item.get("size", list())

                product = ProductModel(
                    id=id,
                    title=title,
                    availability=availability,
                    productDescription=product_description,
                    imageURL=image_url,
                    price=price
                )

                product.categories = []
                product.colors = []
                product.sizes = []

                parent_category = CategoryModel.find_by_level(session, 0)[0]
                for i in range(len(cat_level_names)):

                    current_category = CategoryModel.find_if_exists(session, parent_category.id, cat_level_names[i], i+1)

                    if current_category is None:
                        current_category = CategoryModel(
                            parent_id=parent_category.id,
                            name=cat_level_names[i],
                            level=i+1
                        )

                        current_category.save(session)
                        session.flush()

                    product_category_association = ProductCategoryModel(
                        product_id=id,
                        category_id=current_category.id
                    )

                    product.categories.append(product_category_association)
                    parent_category = current_category

                for color in colors:
                    product.colors.append(ColorModel(product_id=id, product_color=color))

                for size in sizes:
                    product.sizes.append(SizeModel(product_id=id, product_size=size))

                product.save(session)
                # time.sleep(0.02)
            try:
                session.commit()
            except Exception as error:
                print(error)
                session.flush()
                session.rollback()
                return False

        return True
