from flaskapp import db
from flaskapp.dal.category import CategoryDAL


class CategoryService:
    @classmethod
    def find_by_id(cls, id):
        return CategoryDAL.find_by_id(db, id)

    @classmethod
    def find_all_children(cls, id):
        return CategoryDAL.find_all_children(db, id)
