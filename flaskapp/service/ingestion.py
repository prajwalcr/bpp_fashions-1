from flask import current_app

from flaskapp import db
from flaskapp.dal.catalog import CatalogDAL
from flaskapp.service.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.service.CatalogProcessors.JsonCatalogProcessor import JsonCatalogProcessor # Don't remove this import


class IngestionService:
    @classmethod
    def validate_site_key(cls, site_key, input_key):
        return site_key == input_key

    @classmethod
    def get_catalog_processor(cls, extension):
        for catalog_processor in CatalogProcessor.__subclasses__():
            if hasattr(catalog_processor, "SUPPORTED_EXTENSION"):
                supported_extension = catalog_processor.SUPPORTED_EXTENSION
                if supported_extension is not None and supported_extension == extension:
                    return catalog_processor

    def exception_handler(func):
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
    def ingest_catalog(self, id, catalog_processor):
        catalog = CatalogDAL.find_by_id(db, id)

        catalog_processor.load()
        if not catalog_processor.validate():
            catalog.status = catalog_processor.STATUS_CODES.get("VALIDATION_FAILURE", "Unavailable")
            CatalogDAL.save(db, catalog)
            db.commit()
            return

        catalog.status = catalog_processor.STATUS_CODES.get("INGESTING", "Unavailable")
        CatalogDAL.save(db, catalog)
        db.commit()

        if catalog_processor.ingest():
            catalog.status = catalog_processor.STATUS_CODES.get("SUCCESS", "Unavailable")
        else:
            catalog.status = catalog_processor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")

        CatalogDAL.save(db, catalog)
        db.commit()
        return
