from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.DAL.product import ProductDAL
from flaskapp.cache import cache
from flaskapp.database import db
from flaskapp.service.pagination import PaginationService
from flaskapp.service.search import SearchService
from flaskapp.schemas import PlainProductSchema, SearchSchema, ProductListSchema, PaginationSchema
from flaskapp.models import ProductModel
from flaskapp.service.sort import SortService

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

            search_data = SearchService.fire_search_query(search_params)
            status, response = SearchService.parse_search_results(search_data)

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

        sort_field, reverse = SortService.parse_parameters(pagination_params)

        page, rows = PaginationService.parse_parameters(pagination_params)
        if rows is None:
            rows = current_app.config['PRODUCTS_PER_PAGE']

        products, total = ProductDAL.find_all(db, sort_field, reverse, page, rows)

        if total == 0:
            abort(400, message="No match found")

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

        search_data = SearchService.fire_search_query(search_params)
        status, response = SearchService.parse_search_results(search_data)

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
        sort_field, reverse = SortService.parse_parameters(pagination_params)

        page, rows = PaginationService.parse_parameters(pagination_params)
        if rows is None:
            rows = current_app.config['PRODUCTS_PER_PAGE']

        products, total = ProductDAL.find_by_category_id(db, category_id, sort_field, reverse, page, rows)

        if total == 0:
            abort(400, message="No match found")

        response = {
            "total": total,
            "rows": rows,
            "products": [product for product in products]
        }

        return response
