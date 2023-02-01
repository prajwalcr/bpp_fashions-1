from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp import db
from flaskapp.models import ProductCategoryModel, ProductModel, CategoryModel
from flaskapp.schemas import ProductListSchema, PaginationSchema, CategorySchema

blp = Blueprint("category", __name__, description="Operations on product categories")

@blp.route("/api/products/categories/<int:category_id>")
class Category(MethodView):
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, paginationParams, category_id):
        q = db.query(ProductModel) \
            .join(ProductCategoryModel) \
            .filter(ProductCategoryModel.category_id == category_id)


        if "sort" in paginationParams and paginationParams["sort"].lower().split()[0] == "price":
            sortOrder = paginationParams["sort"].lower().split()[-1]

            if sortOrder == "desc":
                q = q.order_by(ProductModel.price.desc())
            else:
                q = q.order_by(ProductModel.price.asc())

        rows = paginationParams.get("rows", current_app.config["PRODUCTS_PER_PAGE"])
        products = q.limit(rows).offset((paginationParams.get("page", 1)-1)*rows).all()

        total = q.count()

        response = {
            "total": total,
            "rows": rows,
            "products": [product for product in products]
        }

        return response


@blp.route("/api/products/categories/children/<int:category_id>")
class CategoryTree(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, category_id):
        if category_id <= 0:
            abort(400, message="Invalid category ID")

        q = db.query(CategoryModel).filter(CategoryModel.parent_id == category_id)

        categories = q.all()

        return categories
