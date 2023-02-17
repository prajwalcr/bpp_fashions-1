from typing import List, Optional

from flaskapp.database import db
from flaskapp.api.catalog.dal.catalog import CatalogDAL
from flaskapp.models import CatalogModel


class CatalogService:
    """Service layer for catalog items."""
    @classmethod
    def find_by_id(cls, id: str) -> CatalogModel:
        """
        Returns a catalog associated with given id.

        Parameters
        ----------
        id: str
            The id of the required catalog.

        Returns
        ----------
        CatalogModel
            The catalog having the given id.
        """

        return CatalogDAL.find_by_id(db, id)

    @classmethod
    def find_all(cls) -> List[CatalogModel]:
        """
        Returns all the catalogs.

        Returns
        ----------
        List[CatalogModel]
            The list of all catalogs.
        """

        return CatalogDAL.find_all(db)

    @classmethod
    def create_and_save(cls, id: str, filepath: Optional[str] = None, status: Optional[str] = None) -> None:
        """
        Create a new catalog and save it to database.

        Parameters
        ----------
        id: str
            Id of the new catalog.
        filepath: str, Optional
            filepath of the new catalog.
        status: str, Optional
            Status of the new catalog.
        """

        catalog = CatalogDAL.create(id, filepath, status)
        CatalogDAL.save(db, catalog)
        db.commit()
