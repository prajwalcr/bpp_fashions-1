from flaskapp.models import ColorModel


class ColorDAL:
    @classmethod
    def create(cls, id, color):
        color = ColorModel(product_id=id, product_color=color)
        return color
