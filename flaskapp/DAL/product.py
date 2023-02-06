from flaskapp.models import ProductModel


class ProductDAL:
    @classmethod
    def find_by_id(cls, db, id):
        return ProductModel.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db, sort_field=None, reverse=False, page=None, rows=None):
        q = ProductModel.find_all_query(db)
        total = ProductModel.count(q)

        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)

        return q.all(), total

    @classmethod
    def find_by_category_id(cls, db, category_id, sort_field=None, reverse=False, page=None, rows=None):
        q = ProductModel.find_by_category_id_query(db, category_id)
        total = ProductModel.count(q)

        q = cls.__sort_by(q, sort_field, reverse)
        q = cls.__paginate(q, page, rows)

        return q.all(), total

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
    def save(cls, db, product):
        product.save(db)
