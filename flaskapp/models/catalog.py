from flaskapp.database import Base
from sqlalchemy import Column, String


class CatalogModel(Base):
    __tablename__ = "catalog"

    id = Column(String(500), primary_key=True)
    status = Column(String(500))
    filepath = Column(String(500), nullable=False)

    def __repr__(self):
        return f"Catalog('{self.id}, '{self.status}')"

    @classmethod
    def find_by_id_query(cls, db, id):
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db):
        return db.query(cls)

    def save(self, db):
        db.add(self)
