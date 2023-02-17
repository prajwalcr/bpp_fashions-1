from flaskapp.models import ProductCategoryModel


class ProductCategoryDAL:
    """Data Access Layer for product-category association objects."""
    @classmethod
    def create(cls, product_id: str, category_id: int) -> ProductCategoryModel:
        """
        Create a new product-category association object.

        Parameters
        ----------
        product_id: str
            The id of the product.
        category_id: int
            The id of the category.

        Returns
        ----------
        ProductCategoryModel
            The new created product-category association object.
        """

        product_category_association = ProductCategoryModel(product_id=product_id, category_id=category_id)
        return product_category_association
