class CatalogProcessor:
    STATUS_CODES = {
        "VALIDATING": "Validating Catalog",
        "INGESTING": "Ingesting Catalog",
        "SUCCESS": "Successfully Ingested Catalog",
        "VALIDATION_FAILURE": "Validation Failed",
        "INGESTION_FAILURE": "Catalog Ingestion Failed"
    }

    def __init__(self, filepath):
        self.filepath = filepath
