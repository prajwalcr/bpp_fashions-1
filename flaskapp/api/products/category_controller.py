from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.database import db
from flaskapp.models import ProductModel, CategoryModel
from flaskapp.schemas import ProductListSchema, PaginationSchema, CategorySchema

blp = Blueprint("category", __name__, description="Operations on product categories")


@blp.route("/api/products/categories/<int:category_id>")
class Category(MethodView):
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, pagination_params, category_id):
        q = ProductModel.find_by_category_id_query(db, category_id)

        if "sort" in pagination_params and pagination_params["sort"].lower().split()[0] == "price":
            sort_order = pagination_params["sort"].lower().split()[-1]

            if sort_order == "desc":
                q = ProductModel.order_by_price_query(q, reverse=True)
            else:
                q = ProductModel.order_by_price_query(q)

        rows = pagination_params.get("rows", current_app.config["PRODUCTS_PER_PAGE"])
        page = pagination_params.get("page", 1)

        products = ProductModel.paginate(q, rows, page)
        total = ProductModel.count(q)

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

        categories = CategoryModel.find_all_children_query(db, category_id)

        return categories
