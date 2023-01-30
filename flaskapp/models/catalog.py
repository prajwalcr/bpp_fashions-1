from flaskapp.database import Base
from sqlalchemy import Column, String

class CatalogModel(Base):
    __tablename__ = "catalog"

    id = Column(String(50), primary_key=True)
    status = Column(String(50))
    filepath = Column(String(200), nullable=False)

    def __repr__(self):
        return f"Catalog('{self.id}, '{self.status}')"
