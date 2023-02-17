from flaskapp.models import SizeModel


class SizeDAL:
    """Data Access Layer for size objects."""
    @classmethod
    def create(cls, id: str, size: str) -> SizeModel:
        """
        Create a new size object.

        Parameters
        ----------
        id: str
            The id of the product having the size.
        size: str
            The name of the new size object.

        Returns
        ----------
        SizeModel
            The new created size object.
        """

        size = SizeModel(product_id=id, product_size=size)
        return size
