from flaskapp.models import ProductCategoryModel


class ProductCategoryDAL:
    @classmethod
    def create(cls, product_id, category_id):
        product_category_association = ProductCategoryModel(product_id=product_id, category_id=category_id)
        return product_category_association
