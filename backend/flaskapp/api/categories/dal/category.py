from flaskapp.models import CategoryModel


class CategoryDAL:
    @classmethod
    def find_by_id(cls, db, id):
        return CategoryModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db):
        return CategoryModel.find_all_query(db).all()

    @classmethod
    def find_by_level(cls, db, level):
        return CategoryModel.find_by_level_query(db, level).all()

    @classmethod
    def find_all_children(cls, db, category_id):
        return CategoryModel.find_all_children_query(db, category_id).all()

    @classmethod
    def find_if_exists(cls, db, parent_id=None, name=None, level=None):
        return CategoryModel.find_if_exists_query(db, parent_id, name, level).first()

    @classmethod
    def create(cls, parent_id=None, name=None, level=None):
        category = CategoryModel(
            parent_id=parent_id,
            name=name,
            level=level
        )
        return category

    @classmethod
    def save(cls, db, category):
        return category.save(db)
