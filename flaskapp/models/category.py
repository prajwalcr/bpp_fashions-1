from flaskapp.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer

class CategoryModel(Base):
    __tablename__ = "category"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(50))
    level = Column(Integer)

    def __repr__(self):
        return f"Category('{self.id}', '{self.parent_id}', '{self.name}', '{self.level}')"
