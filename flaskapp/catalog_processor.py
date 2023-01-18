import json
from flaskapp.models import Product
from flaskapp import db

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

        for dataItem in self.data:
            product = Product(
                id=dataItem["sku"],
                # availability=dataItem["availability"],
                # productDescription=dataItem["productDescription"],
                # imageURL=dataItem["productImage"],
                price=dataItem["price"]
            )

            db.session.add(product)

        db.session.commit()

        return True
