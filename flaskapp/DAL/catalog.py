from flaskapp.models import CatalogModel


class CatalogDAL:
    @classmethod
    def find_by_id(cls, db, id):
        return CatalogModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db):
        return CatalogModel.find_all_query(db).all()

    @classmethod
    def save(cls, db, catalog):
        catalog.save(db)
