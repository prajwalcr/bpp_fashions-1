import os
from flask import Flask
from flask_smorest import Api

from flaskapp.database import db

from flaskapp.api.product import blp as ProductBlueprint
from flaskapp.api.ingestion import blp as IngestionBlueprint

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = os.path.join(app.instance_path, "catalog_dir")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.config['API_TITLE'] = "Store REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024
    app.config['INGESTION_KEY'] = 'dummy'

    api = Api(app)

    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(IngestionBlueprint)

    return app

