import json
from flaskapp.models import Product, Category, Color, Size

from flaskapp import SessionLocal

import time

class CatalogProcessor:
    def __init__(self, filepath):
        self.filepath = filepath


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
            if "sku" not in dataItem:
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
                id = dataItem["sku"]
                title = dataItem.get("title", None)
                if "availability" in dataItem:
                    availability = dataItem["availability"].lower() == "true"
                else:
                    availability = False
                productDescription = dataItem.get("productDescription", None)
                imageURL = dataItem.get("productImage", None) # Replace this maybe
                price = dataItem["price"]

                catlevel1 = dataItem.get("catlevel1Name", None)

                catlevel2 = None
                if "catlevel2Name" in dataItem:
                    catlevel2 = dataItem["catlevel2Name"].strip()

                colors = dataItem.get("color", list())
                sizes = dataItem.get("size", list())

                product = Product(
                    id=id,
                    title=title,
                    availability=availability,
                    productDescription=productDescription,
                    imageURL=imageURL,
                    price=price
                )

                category = Category(
                    product_id=id,
                    catlevel1=catlevel1,
                    catlevel2=catlevel2
                )

                colorList = []
                for color in colors:
                    colorList.append(Color(product_id=id, product_color=color))

                sizeList = []
                for size in sizes:
                    sizeList.append(Size(product_id=id, product_size=size))

                product.category = category
                product.colors = colorList
                product.sizes = sizeList

                session.add(product)
                # time.sleep(0.02)
            try:
                session.commit()
            except Exception as error:
                session.flush()
                session.rollback()
                return False

        return True
