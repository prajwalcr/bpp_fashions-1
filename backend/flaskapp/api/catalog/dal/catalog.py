from flaskapp.models import CatalogModel
from typing import List, Optional

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query

class CatalogDAL:
    """Data Access Layer for catalog objects."""
    @classmethod
    def find_by_id(cls, db: Session, id: str) -> CatalogModel:
        """
        Returns a catalog associated with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        id: str
            The id of the required catalog.

        Returns
        ----------
        CatalogModel
            The catalog having the given id.
        """

        return CatalogModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db: Session) -> List[CatalogModel]:
        """
        Returns all the catalogs.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.

        Returns
        ----------
        List[CatalogModel]
            The list of all catalogs.
        """

        return CatalogModel.find_all_query(db).all()

    @classmethod
    def create(cls, id: str, filepath: Optional[str] = None, status: Optional[str] = None) -> CatalogModel:
        """
        Create a new catalog.

        Parameters
        ----------
        id: str
            Id of the new catalog.
        filepath: str, Optional
            filepath of the new catalog.
        status: str, Optional
            Status of the new catalog.

        Returns
        ----------
        CatalogModel
            Return the newly created catalog.
        """

        catalog = CatalogModel(
            id=id,
            status=status,
            filepath=filepath
        )
        return catalog

    @classmethod
    def save(cls, db: Session, catalog: CatalogModel) -> None:
        """
        Save a catalog.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        catalog: CatalogModel
            The catalog to be saved.
        """

        catalog.save(db)
