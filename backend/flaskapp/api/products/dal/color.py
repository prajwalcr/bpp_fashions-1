from flaskapp.models import ColorModel


class ColorDAL:
    """Data Access Layer for color objects."""
    @classmethod
    def create(cls, id: str, color: str) -> ColorModel:
        """
        Create a new color object.

        Parameters
        ----------
        id: str
            The id of the product having the color.
        color: str
            The name of the color.

        Returns
        ----------
        ColorModel
            The new created color object.
        """

        color = ColorModel(product_id=id, product_color=color)
        return color
