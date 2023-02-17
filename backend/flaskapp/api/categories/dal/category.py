from flaskapp.models import CategoryModel
from typing import List, Optional

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query

class CategoryDAL:
    """Data Access Layer for category objects"""
    @classmethod
    def find_by_id(cls, db: Session, id: int) -> CategoryModel:
        """
        Returns a category with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        id: int
            The id of the required category.

        Returns
        ----------
        CategoryModel
            The category having the given id.
        """

        return CategoryModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db: Session) -> List[CategoryModel]:
        """
        Returns all categories.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.

        Returns
        ----------
        List[CategoryModel]
            List of all categories.
        """

        return CategoryModel.find_all_query(db).all()

    @classmethod
    def find_by_level(cls, db: Session, level: int) -> List[CategoryModel]:
        """
        Returns all categories belonging to given level.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        level: int
            The category level of the required category objects.

        Returns
        ----------
        List[CategoryModel]
            List of all categories of the given level.
        """

        return CategoryModel.find_by_level_query(db, level).all()

    @classmethod
    def find_all_children(cls, db: Session, category_id: int) -> List[CategoryModel]:
        """
        Returns all immediate children of a given category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        category_id: int
            The id of the category whose children are required.

        Returns
        ----------
        List[CategoryModel]
            The list of all immediate children of category of given id.
        """

        return CategoryModel.find_all_children_query(db, category_id).all()

    @classmethod
    def find_if_exists(cls, db: Session, parent_id: Optional[int] = None,
                       name: Optional[str] = None, level: Optional[int] = None) -> CategoryModel:
        """
        Check existence of a given category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        parent_id: int, optional
            The parent id of the category.
        name: str, optional
            The name of the category.
        level: int, optional
            The level of the category.

        Returns
        ----------
        Query
            The category which matches all the parameters, if present.
        """

        return CategoryModel.find_if_exists_query(db, parent_id, name, level).first()

    @classmethod
    def create(cls, parent_id: Optional[int] = None, name: Optional[str] = None,
               level: Optional[int] = None) -> CategoryModel:
        """
       Create a new category.

       Parameters
       ----------
       parent_id: int, Optional
           Parent id of the new category.
       name: str, Optional
           Name of the new category.
       level: int, Optional
           Level of the new category.

       Returns
       ----------
       CategoryModel
           Return the newly created category.
       """

        category = CategoryModel(
            parent_id=parent_id,
            name=name,
            level=level
        )
        return category

    @classmethod
    def save(cls, db: Session, category: CategoryModel) -> None:
        """
        Save a category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        category: CategoryModel
            The category to be saved.
        """

        category.save(db)
