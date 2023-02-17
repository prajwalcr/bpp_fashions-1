from typing import List

from flaskapp.database import db
from flaskapp.api.categories.dal.category import CategoryDAL
from flaskapp.models import CategoryModel


class CategoryService:
    """Service layer for categories."""
    @classmethod
    def find_by_id(cls, id: int) -> CategoryModel:
        """
        Returns a category with given id.

        Parameters
        ----------
        id: int
            The id of the required category.

        Returns
        ----------
        CategoryModel
            The category having the given id.
        """

        return CategoryDAL.find_by_id(db, id)

    @classmethod
    def find_all_children(cls, id: int) -> List[CategoryModel]:
        """
        Returns all immediate children of a given category.

        Parameters
        ----------
        id: int
            The id of the category whose children are required.

        Returns
        ----------
        List[CategoryModel]
            The list of all immediate children of category of given id.
        """

        return CategoryDAL.find_all_children(db, id)
