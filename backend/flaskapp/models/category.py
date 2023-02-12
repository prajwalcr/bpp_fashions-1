from flaskapp.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Sequence


class CategoryModel(Base):
    __tablename__ = "category"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, Sequence("my_sequence"), primary_key=True)
    parent_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(50))
    level = Column(Integer)

    def __repr__(self):
        return f"Category('{self.id}', '{self.parent_id}', '{self.name}', '{self.level}')"

    @classmethod
    def find_by_id_query(cls, db, id):
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db):
        return db.query(cls)

    @classmethod
    def find_by_level_query(cls, db, level):
        return db.query(cls).filter(cls.level == level)

    @classmethod
    def find_all_children_query(cls, db, category_id):
        return db.query(cls).filter(cls.parent_id == category_id)

    @classmethod
    def find_if_exists_query(cls, db, parent_id=None, name=None, level=None):
        q = db.query(cls)
        if parent_id is not None:
            q = q.filter(cls.parent_id == parent_id)
        if name is not None:
            q = q.filter(cls.name == name)
        if level is not None:
            q = q.filter(cls.level == level)
        return q

    def save(self, db):
        db.add(self)
