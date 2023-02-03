from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.cache import cache
from flaskapp.database import db
from flaskapp.api.products.search import SearchHelper
from flaskapp.schemas import PlainProductSchema, SearchSchema, ProductListSchema, PaginationSchema
from flaskapp.models import ProductModel
from flaskapp.utils import pagination_page_limit

blp = Blueprint("product", __name__, description="Operations on products")


@cache.cached(query_string=True)
@blp.route("/api/products/<string:product_id>")
class Product(MethodView):
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        q = ProductModel.find_by_id_query(db, product_id)

        if q.first() is None:
            search_params = {
                "q": product_id
            }

            search_data = SearchHelper.fire_search_query(search_params)
            status, response = SearchHelper.parse_search_results(search_data)

            if status != 200:
                abort(status, message=response)

            if response["total"] < 1:
                abort(404, message="Resource not found")

            return response["products"][0]

        product = q.first()

        return product


@cache.cached(query_string=True)
@blp.route("/api/products")
class ProductList(MethodView):
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, pagination_params):
        q = ProductModel.find_all_query(db)

        if "sort" in pagination_params and pagination_params["sort"].lower().split()[0] == "price":
            sort_order = pagination_params["sort"].lower().split()[-1]

            if sort_order == "desc":
                q = ProductModel.order_by_price_query(q, reverse=True)
            else:
                q = ProductModel.order_by_price_query(q)

        page = pagination_params.get("page", 1)
        rows = pagination_params.get("rows", current_app.config["PRODUCTS_PER_PAGE"])

        products = ProductModel.paginate(q, rows, page)
        total = ProductModel.count(q)

        if total != 0 and page > pagination_page_limit(rows, total):
            abort(400, message="Page number too high")

        response = {
            "total": total,
            "rows": rows,
            "products": products
        }

        return response


@cache.cached(query_string=True)
@blp.route("/api/search")
class ProductSearch(MethodView):
    @blp.arguments(SearchSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, search_params):
        if "rows" not in search_params:
            search_params["rows"] = current_app.config["PRODUCTS_PER_PAGE"]

        search_data = SearchHelper.fire_search_query(search_params)
        status, response = SearchHelper.parse_search_results(search_data)

        if status != 200:
            abort(status, message=response)

        response["rows"] = search_params["rows"]

        return response


@cache.cached(query_string=True)
@blp.route("/api/products/categories/<int:category_id>")
class ProductCategory(MethodView):
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

        if total != 0 and page > pagination_page_limit(rows, total):
            abort(400, message="Page number too high")

        response = {
            "total": total,
            "rows": rows,
            "products": [product for product in products]
        }

        return response
