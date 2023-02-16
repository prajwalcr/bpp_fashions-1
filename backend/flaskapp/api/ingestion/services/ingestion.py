from typing import Type

from flaskapp.database import db
from flaskapp.api.catalog.dal.catalog import CatalogDAL
from flaskapp.api.ingestion.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.api.ingestion.CatalogProcessors.JsonCatalogProcessor import JsonCatalogProcessor # Do not remove this import


class IngestionService:
    """Service layer for ingesting catalogs."""
    @classmethod
    def validate_site_key(cls, site_key: str, input_key: str) -> bool:
        """
        Validate the site key passed by the customer.

        Parameters
        ----------
        site_key: str
            Unbxd's site key for the customer's website
        input_key: str
            Input key passed by the customer

        Returns
        -------
        bool
            Returns True if customer's input key is valid, else False
        """
        return site_key == input_key

    @classmethod
    def get_catalog_processor(cls, extension: str) -> Type[CatalogProcessor]:
        """
        Obtain the catalog processor that is compatible with the type of the catalog file to be parsed.

        Parameters
        ----------
        extension: str
            Type of the catalog file to be parsed.

        Returns
        -------
        CatalogProcessor
            Catalog processor that is compatible with the catalog file type.
        """

        # Find a catalog processor that supports the catalog file type.
        # The 'SUPPORTED_EXTENSION' attribute of the catalog processor specified which file type it supports.
        for catalog_processor in CatalogProcessor.__subclasses__():
            if hasattr(catalog_processor, "SUPPORTED_EXTENSION"):
                supported_extension = catalog_processor.SUPPORTED_EXTENSION
                if supported_extension is not None and supported_extension == extension:
                    return catalog_processor

    def exception_handler(func):
        """Wrapper function to handle any errors in decorated functions"""
        from functools import wraps

        @wraps(func)
        def inner_function(self, id, *args, **kwargs):
            try:
                return func(self, id, *args, **kwargs)
            except Exception as e:
                print(f"Exception in {func.__name__}:", e)

                catalog = CatalogDAL.find_by_id(db, id)
                catalog.status = CatalogProcessor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")
                CatalogDAL.save(db, catalog)
                db.commit()

        return inner_function

    @exception_handler
    def ingest_catalog(self, id: str, catalog_processor: Type[CatalogProcessor]) -> None:
        """
        Ingest a given catalog into database.

        Parameters
        ----------
        id: str
            Id of the catalog to be ingested.
        catalog_processor: Type[CatalogProcessor]
            Catalog processor to ingest the catalog file
        """

        catalog = CatalogDAL.find_by_id(db, id)

        # Load the catalog contents.
        catalog_processor.load()

        valid_catalog = catalog_processor.validate()
        if not valid_catalog:
            catalog.status = catalog_processor.STATUS_CODES.get("VALIDATION_FAILURE", "Unavailable")
            CatalogDAL.save(db, catalog)
            db.commit()
            return

        catalog.status = catalog_processor.STATUS_CODES.get("INGESTING", "Unavailable")
        CatalogDAL.save(db, catalog)
        db.commit()

        catalog_ingestion_done = catalog_processor.ingest()
        if catalog_ingestion_done:
            catalog.status = catalog_processor.STATUS_CODES.get("SUCCESS", "Unavailable")
        else:
            catalog.status = catalog_processor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")

        CatalogDAL.save(db, catalog)
        db.commit()
        return
