import os

from flask import Flask
from flask_smorest import Api

from flaskapp.api.products.product_controller import blp as ProductBlueprint
from flaskapp.api.categories.category_controller import blp as CategoryBlueprint
from flaskapp.api.ingestion.ingestion_controller import blp as IngestionBlueprint
from flaskapp.api.catalog.catalog_controller import blp as CatalogBlueprint
from flaskapp.cache import cache
from dotenv import load_dotenv


load_dotenv()


def create_app():
    """Factory pattern for creating flask app."""
    app = Flask(__name__)

    # Path where product catalogs will be uploaded.
    UPLOAD_FOLDER = os.path.join(app.instance_path, "catalog_dir")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.config['API_TITLE'] = "Store REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/api/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024

    app.config['SITE_KEY'] = os.environ['SITE_KEY']
    app.config['UNBXD_API_KEY'] = os.environ['UNBXD_API_KEY']
    app.config['UNBXD_SEARCH_URL'] = 'https://search.unbxd.io/'

    app.config['PRODUCTS_PER_PAGE'] = 9

    app.config['CACHE_TYPE'] = os.environ['CACHE_TYPE']
    app.config['CACHE_REDIS_HOST'] = os.environ['CACHE_REDIS_HOST']
    app.config['CACHE_REDIS_PORT'] = os.environ['CACHE_REDIS_PORT']
    app.config['CACHE_REDIS_DB'] = os.environ['CACHE_REDIS_DB']
    app.config['CACHE_REDIS_URL'] = os.environ['CACHE_REDIS_URL']
    app.config['CACHE_DEFAULT_TIMEOUT'] = os.environ['CACHE_DEFAULT_TIMEOUT']

    initialize_extensions(app)

    api = Api(app)

    register_blueprints(api)

    return app


def initialize_extensions(app):
    """Initialize flask app extensions"""
    cache.init_app(app)


def register_blueprints(api):
    """Register created blueprints to the app"""
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(IngestionBlueprint)
    api.register_blueprint(CatalogBlueprint)
