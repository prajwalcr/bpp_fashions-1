from flaskapp.database import db
from flaskapp.api.products.dal.product import ProductDAL
from flask import current_app
from typing import Union, List, Tuple

from flaskapp.models import ProductModel


class ProductService:
    """Service layer for products."""
    @classmethod
    def parse_sort_parameters(cls, parameters: dict) -> Union[Tuple[str, bool], Tuple[None, None]]:
        """
        Extract sort parameters from the product query parameters, if present

        Parameters
        ----------
        parameters: dict
            Contains parameters for sorting or paginating the products result.

        Returns
        ----------
        str
            The attribute on which to sort the products.
        bool
            The order in which to sort. If true, products are returned in descending order.
        """

        if "sort" in parameters and parameters["sort"].lower().split()[0] == "price":
            sort_field = "price"
            sort_order = parameters["sort"].lower().split()[-1]
            reverse = False

            if sort_order == "desc":
                reverse = True

            return sort_field, reverse

        return None, None

    @classmethod
    def parse_pagination_parameters(cls, parameters: dict) -> Tuple[int, int]:
        """
        Extract paginations parameters from the product query parameters, if present

        Parameters
        ----------
        parameters: dict
            Contains parameters for sorting or paginating the products result.

        Returns
        ----------
        int
            Offset or page number from which products are displayed.
        int
            Number of products to display at a time on a single page.
        """

        app = current_app._get_current_object()
        page = parameters.get("page", 1)
        rows = parameters.get("rows", app.config['PRODUCTS_PER_PAGE'])
        return page, rows

    @classmethod
    def find_by_id(cls, id: str) -> ProductModel:
        """
        Find a product with given id.

        Parameters
        ----------
        id: str
            The id of the required product.

        Returns
        ----------
        ProductModel
            The product having the given id.
        """

        return ProductDAL.find_by_id(db, id)

    @classmethod
    def find_all(cls, parameters: dict) -> Tuple[List[ProductModel], int]:
        """
        Returns all products after sorting and paginating, if required.

        Performs sorting if sort_field attribute is provided in parameters.
        Performs pagination if page and rows attributes are provided in parameters.

        Parameters
        ----------
        parameters: dict
            Contains parameters for sorting or paginating the products result.

        Returns
        ----------
        List[ProductModel]
            The list of all products sorted and paginated as requested.
        int
            The total number of products present.
        """

        sort_field, reverse = cls.parse_sort_parameters(parameters)
        page, rows = cls.parse_pagination_parameters(parameters)

        products = ProductDAL.find_all(db, sort_field, reverse, page, rows)
        total = ProductDAL.count_all(db)

        return products, total

    @classmethod
    def find_by_category(cls, category_id: int, parameters: dict) -> Tuple[List[ProductModel], int]:
        """
        Returns all products belonging to the specified category after sorting and paginating, if required.

        Performs sorting if sort_field attribute is provided in parameters.
        Performs pagination if page and rows attributes are provided in parameters.

        Parameters
        ----------
        category_id: int
            The id of the category of the required products.
        parameters: dict
            Contains parameters for sorting or paginating the products result.

        Returns
        ----------
        List[ProductModel]
            The list of all products sorted and paginated as requested.
        int
            The total number of products present.
        """

        sort_field, reverse = cls.parse_sort_parameters(parameters)
        page, rows = cls.parse_pagination_parameters(parameters)

        products = ProductDAL.find_by_category_id(db, category_id, sort_field, reverse, page, rows)
        total = ProductDAL.count_by_category_id(db, category_id)

        return products, total
