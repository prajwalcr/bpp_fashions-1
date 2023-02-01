import json
from flaskapp.models import ProductModel, CategoryModel, ColorModel, SizeModel, ProductCategoryModel
from flaskapp.api.ingestion.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.database import SessionLocal


class JsonCatalogProcessor(CatalogProcessor):
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

        for dataItem in self.data:
            if type(dataItem) != dict:
                return False
            if "uniqueId" not in dataItem:
                return False
            if "price" not in dataItem:
                return False

        return True

    def ingest(self):
        if self.data is None:
            return False

        # Session = db.sessionmaker()
        with SessionLocal() as session:

            for dataItem in self.data:
                id = dataItem["uniqueId"]
                title = dataItem.get("title", None)
                if "availability" in dataItem:
                    availability = dataItem["availability"].lower() == "true"
                else:
                    availability = False
                productDescription = dataItem.get("productDescription", None)
                imageURL = dataItem.get("productImage", None) # Replace this maybe
                price = dataItem["price"]

                catLevelNames = []
                levelCounter = 1
                while True:
                    field = "catlevel"+str(levelCounter)+"Name"
                    if field not in dataItem:
                        break
                    catLevelNames.append(dataItem[field].strip())
                    levelCounter += 1

                colors = dataItem.get("color", list())
                sizes = dataItem.get("size", list())

                product = ProductModel(
                    id=id,
                    title=title,
                    availability=availability,
                    productDescription=productDescription,
                    imageURL=imageURL,
                    price=price
                )

                product.categories = []
                product.colors = []
                product.sizes = []

                parentCategory = session.query(CategoryModel).filter(CategoryModel.level == 0).first()
                for i in range(len(catLevelNames)):

                    currentCategory = session.query(CategoryModel)\
                        .filter(CategoryModel.parent_id == parentCategory.id)\
                        .filter(CategoryModel.name == catLevelNames[i])\
                        .filter(CategoryModel.level == i+1)\
                        .first()

                    if currentCategory is None:
                        currentCategory = CategoryModel(
                            parent_id=parentCategory.id,
                            name=catLevelNames[i],
                            level=i+1
                        )

                        session.add(currentCategory)
                        session.flush()

                    product_category_association = ProductCategoryModel(
                        product_id=id,
                        category_id=currentCategory.id
                    )

                    product.categories.append(product_category_association)
                    parentCategory = currentCategory

                for color in colors:
                    product.colors.append(ColorModel(product_id=id, product_color=color))

                for size in sizes:
                    product.sizes.append(SizeModel(product_id=id, product_size=size))

                session.add(product)
                # time.sleep(0.02)
            try:
                session.commit()
            except Exception as error:
                session.flush()
                session.rollback()
                return False

        return True