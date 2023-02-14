from flaskapp import db
from flaskapp.dal.catalog import CatalogDAL


class CatalogService:
    @classmethod
    def find_by_id(cls, id):
        return CatalogDAL.find_by_id(db, id)

    @classmethod
    def find_all(cls):
        return CatalogDAL.find_all(db)

    @classmethod
    def create_and_save(cls, id, filepath=None, status=None):
        catalog = CatalogDAL.create(id, filepath, status)
        CatalogDAL.save(db, catalog)
        db.commit()
