from flaskapp.models import SizeModel


class SizeDAL:
    @classmethod
    def create(cls, id, size):
        color = SizeModel(product_id=id, product_size=size)
        return color
