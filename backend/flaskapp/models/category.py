from flaskapp.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Sequence

from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


class CategoryModel(Base):
    """ORM class for category objects."""
    __tablename__ = "category"

    id = Column(Integer, Sequence("my_sequence"), primary_key=True)
    parent_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(50))
    level = Column(Integer)

    def __repr__(self):
        """Returns a readable representation of a category object."""
        return f"Category('{self.id}', '{self.parent_id}', '{self.name}', '{self.level}')"

    @classmethod
    def find_by_id_query(cls, db: Session, id: int) -> Query:
        """
        Returns a category object associated with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        id: int
            The id of the required category object.

        Returns
        ----------
        Query
            The query for finding category object by id.
        """
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db: Session) -> Query:
        """
        Returns all category objects.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.

        Returns
        ----------
        Query
            The query for finding all category objects present in the database.
        """

        return db.query(cls)

    @classmethod
    def find_by_level_query(cls, db: Session, level: int) -> Query:
        """
        Returns all category objects belonging to given level.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        level: int
            The category level of the required category objects.

        Returns
        ----------
        Query
            The query for finding all category objects of the given level.
        """

        return db.query(cls).filter(cls.level == level)

    @classmethod
    def find_all_children_query(cls, db: Session, category_id: int):
        """
        Returns all immediate children of a given category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        category_id: int
            The id of the category object whose children are required.

        Returns
        ----------
        Query
            The query for finding all immediate children of category object of given id.
        """

        return db.query(cls).filter(cls.parent_id == category_id)

    @classmethod
    def find_if_exists_query(cls, db: Session, parent_id: Optional[int] = None,
                             name: Optional[str] = None, level: Optional[int] = None) -> Query:
        """
        Check existence of a given category object.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        parent_id: int, optional
            The parent id of the category object.
        name: str, optional
            The name of the category object.
        level: int, optional
            The level of the category object.

        Returns
        ----------
        Query
            The query for returning all matching objects.
        """

        q = db.query(cls)
        if parent_id is not None:
            q = q.filter(cls.parent_id == parent_id)
        if name is not None:
            q = q.filter(cls.name == name)
        if level is not None:
            q = q.filter(cls.level == level)
        return q

    def save(self, db: Session) -> None:
        """
        Save a category object.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        """

        db.add(self)
