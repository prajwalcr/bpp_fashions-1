from flaskapp.database import Base
from sqlalchemy import Column, String

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


class CatalogModel(Base):
    """ORM class for catalog objects."""
    __tablename__ = "catalog"

    id = Column(String(500), primary_key=True)
    status = Column(String(500))
    filepath = Column(String(500), nullable=False)

    def __repr__(self):
        """Returns a readable representation of a catalog object."""
        return f"Catalog('{self.id}, '{self.status}')"

    @classmethod
    def find_by_id_query(cls, db: Session, id: str) -> Query:
        """
        Returns a catalog object associated with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        id: str
            The id of the required catalog object.

        Returns
        ----------
        Query
            The query for finding catalog object by id.
        """

        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db: Session) -> Query:
        """
        Returns all catalog objects.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.

        Returns
        ----------
        Query
            The query for finding all catalog objects present in the database.
        """

        return db.query(cls)

    def save(self, db: Session) -> None:
        """
        Save a catalog object.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        """

        db.add(self)
