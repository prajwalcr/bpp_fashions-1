from flaskapp.database import Base
from sqlalchemy import Column, String, Boolean, Text, Float
from sqlalchemy.orm import relationship
from flaskapp.models.product_category import ProductCategoryModel

from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


class ProductModel(Base):
    """ORM class for product objects."""
    __tablename__ = "product"

    id = Column(String(15), primary_key=True)
    title = Column(String(80))
    availability = Column(Boolean)
    productDescription = Column(Text)
    imageURL = Column(Text)
    price = Column(Float)
    categories = relationship("ProductCategoryModel", backref="product", uselist=True)
    sizes = relationship("SizeModel", backref="product", lazy=True)
    colors = relationship("ColorModel", backref="product", lazy=True)

    def __repr__(self):
        """Returns a readable representation of a product object."""
        return f"Product('{self.id}', '{self.title}, '{self.price}')"

    @classmethod
    def find_by_id_query(cls, db: Session, id: str) -> Query:
        """
        Returns a product object associated with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        id: str
            The id of the required product object.

        Returns
        ----------
        Query
            The query for finding product object by id.
        """
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db: Session) -> Query:
        """
        Returns all product objects.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.

        Returns
        ----------
        Query
            The query for finding all product objects present in the database.
        """

        return db.query(cls)

    @classmethod
    def find_by_category_id_query(cls, db: Session, category_id: int) -> Query:
        """
        Returns all product objects belonging to a specific category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        category_id: int
            The id of the category of the required products.

        Returns
        ----------
        Query
            The query for finding all product objects belonging to a specific category.
        """

        return db.query(cls) \
            .join(ProductCategoryModel) \
            .filter(ProductCategoryModel.category_id == category_id)

    @classmethod
    def order_by_price_query(cls, q: Query, reverse: Optional[bool] = False) -> Query:
        """
        Orders queried products by price.

        Parameters
        ----------
        q: Query
            The query whose results need to be ordered.
        reverse: bool, optional
            If reverse is True, sort in descending order else in ascending order. Defaults to False.

        Returns
        ----------
        Query
            The query for ordering results of the original query.
        """

        if reverse:
            return q.order_by(cls.price.desc())
        return q.order_by(cls.price)

    @classmethod
    def paginate_query(cls, q: Query, rows: int, page: int) -> Query:
        """
        Paginates resulting products.

        Parameters
        ----------
        q: Query
            The query whose results need to be paginated.
        rows: int
            Number of products to display at a time on a single page.
        page: int
            Offset or page number from which products are displayed.

        Returns
        ----------
        Query
            The query for paginating results of the original query.
        """

        return q.limit(rows).offset((page - 1) * rows)

    @classmethod
    def count(cls, q: Query) -> int:
        """
        Calculate total number of products resulting from a query.

        Parameters
        ----------
        q: Query
            The query for which number of products need to be calculated.

        Returns
        ----------
        int
            The number of products resulting from the query.
        """

        return q.count()

    def save(self, db: Session) -> None:
        """
        Save a product object.

        Parameters
        ----------
        db: Session
            The database session in which to execute the query.
        """

        db.add(self)
