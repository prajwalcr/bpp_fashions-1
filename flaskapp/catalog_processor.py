import json

class CatalogProcessor:
    def __init__(self, filepath):
        self.filepath = filepath


class JsonCatalogProcessor(CatalogProcessor):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = None

    def load(self):
        f = open(self.filepath)
        try:
            self.data = json.load(f)
        except ValueError:
            pass

    def validate(self):
        if self.data is None:
            return False

        if type(self.data) != list:
            return False

        for product in self.data:
            if type(product) != dict:
                return False
            if "sku" not in product:
                return False
            if "price" not in product:
                return False

        return True

    def ingest(self):
        return True
