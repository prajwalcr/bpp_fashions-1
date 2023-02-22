from flaskapp.models import ProductModel
from typing import List, Optional
import pandas as pd

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import select
from sqlalchemy.engine import Engine


class ProductDAL:
    """Data Access Layer for product objects."""
    @classmethod
    def find_by_id(cls, db: Session, id: str) -> ProductModel:
        """
        Find a product with given id.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        id: str
            The id of the required product.

        Returns
        ----------
        ProductModel
            The product having the given id.
        """

        return ProductModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db: Session, sort_field: Optional[str] = None, reverse: Optional[bool] = False,
                 page: Optional[int] = None, rows: Optional[int] = None) -> List[ProductModel]:
        """
        Returns all products after sorting and paginating, if required.

        Performs sorting if sort_field is provided.
        Performs pagination if page and rows are provided.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        sort_field: str, Optional
            The attribute of the product on which to sort.
        reverse: bool, Optional
            If reverse is True, sort in descending order else in ascending order. Defaults to False.
        page: int
            Offset or page number from which products are displayed.
        rows: int
            Number of products to display at a time on a single page.

        Returns
        ----------
        List[ProductModel]
            The list of all products sorted and paginated as requested.
        """

        q = ProductModel.find_all_query(db)
        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)
        return q.all()

    @classmethod
    def find_all_df(cls, db: Session, engine: Engine) -> pd.DataFrame:
        """
        Returns pandas dataframe with all products.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.

        engine: Engine
            The connection to the database.

        Returns
        ----------
        Dataframe
            The list of all products in a pandas dataframe containing id and description.
        """
        q = select(ProductModel.id, ProductModel.productDescription)
        return pd.read_sql(sql=q, con=engine)

    @classmethod
    def find_by_category_id(cls, db: Session, category_id: int, sort_field: Optional[str] = None, reverse: Optional[bool] = False,
                 page: Optional[int] = None, rows: Optional[int] = None) -> List[ProductModel]:
        """
        Find all products belonging to a specific category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        category_id: int
            The id of the category of the required products.
        sort_field: str, Optional
            The attribute of the product on which to sort.
        reverse: bool, Optional
            If reverse is True, sort in descending order else in ascending order. Defaults to False.
        page: int
            Offset or page number from which products are displayed.
        rows: int
            Number of products to display at a time on a single page.

        Returns
        ----------
        Query
            The list of all products belonging to specified category, sorted and paginated as requested.
        """

        q = ProductModel.find_by_category_id_query(db, category_id)
        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)
        return q.all()

    @classmethod
    def count_all(cls, db: Session) -> int:
        """
        Calculate total number of all products.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.

        Returns
        ----------
        int
            The total number of products present.
        """

        q = ProductModel.find_all_query(db)
        return ProductModel.count(q)

    @classmethod
    def count_by_category_id(cls, db: Session, category_id: int) -> int:
        """
        Calculate total number of products belonging to given category.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        category_id: int
            The id of the category of the required products.

        Returns
        ----------
        int
            The total number of products belonging to given category.
        """

        q = ProductModel.find_by_category_id_query(db, category_id)
        return ProductModel.count(q)

    @classmethod
    def __sort_by(cls, q: Query, sort_field: str, reverse: bool) -> Query:
        """
        Sort queried products according to a specified attribute.

        Parameters
        ----------
        q: Query
            The query whose results need to be sorted.
        sort_field: str
            The attribute of the product on which to sort.
        reverse: bool
            If reverse is True, sort in descending order else in ascending order.

        Returns
        ----------
        Query
            The query for sorting results of the original query.
        """

        if sort_field is not None:
            if sort_field == "price":
                q = ProductModel.order_by_price_query(q, reverse)
        return q

    @classmethod
    def __paginate(cls, q: Query, page: int, rows: int) -> Query:
        """
        Paginates resulting products.

        Parameters
        ----------
        q: Query
            The query whose results need to be paginated.
        page: int
            Offset or page number from which products are displayed.
        rows: int
            Number of products to display at a time on a single page.

        Returns
        ----------
        Query
            The query for paginating results of the original query.
        """

        if page is not None and rows is not None:
            q = ProductModel.paginate_query(q, rows, page)
        return q

    @classmethod
    def create(cls, id: str, title: Optional[str] = None, availability: Optional[bool] = None,
               product_description: Optional[str] = None, image_url: Optional[str] = None,
               price: Optional[float] = None, product_category_associations: Optional[list] = [],
               colors: Optional[list] = [], sizes: Optional[list] = []) -> ProductModel:
        """
        Create a new product.

        Parameters
        ----------
        id: str
            Id of the new product.
        title: str, Optional
            Title of the new product.
        availability: bool, Optional
            Availability of the new product.
        product_description: str, Optional
            Description of the new product.
        image_url: str, Optional
            URL to the image of the new product.
        price: float, Optional
            Price of the new product.
        product_category_associations: list, Optional
            List of categories to which the product belongs.
        colors: list, Optional
            List of colors of the product.
        sizes: list, Optional
            List of sizes of the product.

        Returns
        ----------
        ProductModel
            Return the newly created product.
        """

        product = ProductModel(
            id=id,
            title=title,
            availability=availability,
            productDescription=product_description,
            imageURL=image_url,
            price=price
        )
        product.categories = product_category_associations
        product.colors = colors
        product.sizes = sizes
        return product

    @classmethod
    def save(cls, db: Session, product: ProductModel) -> None:
        """
        Save a product.

        Parameters
        ----------
        db: Session
            The database session in which to execute the operation.
        product: ProductModel
            The product to be saved.
        """

        product.save(db)
