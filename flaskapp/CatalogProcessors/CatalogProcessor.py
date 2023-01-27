class CatalogProcessor:
    STATUS_CODES = {
        "VALIDATING": "",
        "INGESTING": "",
        "SUCCESS": "",
        "VALIDATION_FAILURE": "Validation Failed",
        "INGESTION_FAILURE": "Catalog Ingestion Failed"
    }

    def __init__(self, filepath):
        self.filepath = filepath
