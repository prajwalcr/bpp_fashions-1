from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.DAL.category import CategoryDAL
from flaskapp.cache import cache
from flaskapp.database import db
from flaskapp.schemas import CategorySchema

blp = Blueprint("category", __name__, description="Operations on product categories")


@cache.cached(query_string=True)
@blp.route("/api/categories/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryDAL.find_by_id(db, category_id)

        if category is None:
            abort(404, message="Resource not found")

        return category


@cache.cached(query_string=True)
@blp.route("/api/categories/children/<int:category_id>")
class CategoryTree(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, category_id):
        if category_id <= 0:
            abort(400, message="Invalid category ID")

        categories = CategoryDAL.find_all_children(db, category_id)

        return categories
