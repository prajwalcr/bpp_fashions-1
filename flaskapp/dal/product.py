from flaskapp.models import ProductModel


class ProductDAL:
    @classmethod
    def find_by_id(cls, db, id):
        return ProductModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db, sort_field=None, reverse=False, page=None, rows=None):
        q = ProductModel.find_all_query(db)
        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)
        return q.all()

    @classmethod
    def find_by_category_id(cls, db, category_id, sort_field=None, reverse=False, page=None, rows=None):
        q = ProductModel.find_by_category_id_query(db, category_id)
        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)
        return q.all()

    @classmethod
    def count_all(cls, db):
        q = ProductModel.find_all_query(db)
        return ProductModel.count(q)

    @classmethod
    def count_by_category_id(cls, db, category_id):
        q = ProductModel.find_by_category_id_query(db, category_id)
        return ProductModel.count(q)

    @classmethod
    def __sort_by(cls, q, sort_field, reverse):
        if sort_field is not None:
            if sort_field == "price":
                q = ProductModel.order_by_price_query(q, reverse)
        return q

    @classmethod
    def __paginate(cls, q, page, rows):
        if page is not None and rows is not None:
            q = ProductModel.paginate_query(q, rows, page)
        return q

    @classmethod
    def create(cls, id, title=None, availability=None, product_description=None, image_url=None, price=None, product_category_associations=[], colors=[], sizes=[]):
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
    def save(cls, db, product):
        return product.save(db)
