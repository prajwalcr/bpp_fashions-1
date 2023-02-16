from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.api.catalog.schema import CatalogSchema
from flaskapp.api.catalog.services.catalog import CatalogService

blp = Blueprint("catalog", __name__, description="Operations on ingestion catalog and its status")


@blp.route("/api/catalog/<string:catalog_id>")
class Catalog(MethodView):
    """Controller class for handling requests on catalog."""
    @blp.response(200, CatalogSchema)
    def get(self, catalog_id: str):
        catalog = CatalogService.find_by_id(catalog_id)

        if catalog is None:
            abort(404, message="Resource not found")

        return catalog
