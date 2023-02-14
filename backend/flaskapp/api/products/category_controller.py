from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.cache import cache
from flaskapp.schemas import CategorySchema
from flaskapp.service.category import CategoryService

blp = Blueprint("category", __name__, description="Operations on product categories")


@blp.route("/api/categories/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryService.find_by_id(category_id)

        if category is None:
            abort(404, message="Resource not found")

        return category


@blp.route("/api/categories/<int:category_id>/children")
class CategoryTree(MethodView):
    @blp.response(200, CategorySchema(many=True))
    @cache.cached(query_string=True)
    def get(self, category_id):
        if category_id < 0:
            abort(400, message="Invalid category ID")

        categories = CategoryService.find_all_children(category_id)

        return categories
