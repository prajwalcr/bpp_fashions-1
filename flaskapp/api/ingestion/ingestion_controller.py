from flask import request, jsonify, current_app
from flask.views import MethodView

from flaskapp.DAL.catalog import CatalogDAL
from flaskapp.database import SessionLocal
from flask_smorest import Blueprint, abort

from flaskapp.models import CatalogModel
from flaskapp.utils import validate_site_key, get_file_extension
from werkzeug.utils import secure_filename
from flaskapp.service.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.service.CatalogProcessors.JsonCatalogProcessor import JsonCatalogProcessor # Don't remove this import
from flaskapp.schemas import MultiPartFileSchema

from threading import Thread
import uuid
import os

db = SessionLocal()
blp = Blueprint("ingestion", __name__, description="Ingest catalog into system")


@blp.route("/api/upload-catalog/<string:site_key>")
class IngestCatalog(MethodView):
    @blp.arguments(MultiPartFileSchema, location="files")
    @blp.response(201)
    def post(self, files, site_key):
        if not validate_site_key(site_key):
            abort(401, message="Invalid Site Key")
        if request.method == "POST":
            if "file" not in files:
                abort(400, message="No File Selected")

            file = files["file"]

            extension = get_file_extension(file.filename)
            if extension is None:
                abort(400, message="Invalid File")

            catalog_processor_class = self.get_catalog_processor(extension)
            if catalog_processor_class is None:
                abort(400, message="File Type Not Supported")

            filepath = self.save_file(file)
            if filepath is None:
                abort(400, "No File Selected")

            catalog_processor = catalog_processor_class(filepath)
            tracking_id = str(uuid.uuid4().hex)

            catalog = CatalogModel(id=tracking_id,
                                   status=catalog_processor_class.STATUS_CODES.get("VALIDATING", "Unavailable"),
                                   filepath=filepath)
            catalog.save(db)
            db.commit()

            response = {
                "message": "File Uploaded Successfully",
                "tracking ID": tracking_id
            }

            try:
                Thread(target=self.ingest_catalog, args=(tracking_id, catalog_processor)).start()
            except Exception as e:
                print("Exception in ingestion:", e)

            return jsonify(response)

    @staticmethod
    def save_file(file):
        if file and file.filename == '':
            return

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath

    @staticmethod
    def get_catalog_processor(extension):
        for catalog_processor in CatalogProcessor.__subclasses__():
            if hasattr(catalog_processor, "SUPPORTED_EXTENSION"):
                supported_extension = catalog_processor.SUPPORTED_EXTENSION
                if supported_extension is not None and supported_extension == extension:
                    return catalog_processor

    def exception_handler(func):
        from functools import wraps

        @wraps(func)
        def inner_function(self, id, *args, **kwargs):
            try:
                return func(self, id, *args, **kwargs)
            except Exception as e:
                print(f"Exception in {func.__name__}:", e)

                catalog = CatalogDAL.find_by_id(db, id)
                catalog.status = CatalogProcessor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")
                catalog.save(db)
                db.commit()

        return inner_function

    @exception_handler
    def ingest_catalog(self, id, catalog_processor):
        catalog = CatalogDAL.find_by_id(db, id)

        catalog_processor.load()
        if not catalog_processor.validate():
            catalog.status = catalog_processor.STATUS_CODES.get("VALIDATION_FAILURE", "Unavailable")
            catalog.save(db)
            db.commit()
            return

        catalog.status = catalog_processor.STATUS_CODES.get("INGESTING", "Unavailable")
        catalog.save(db)
        db.commit()

        if catalog_processor.ingest():
            catalog.status = catalog_processor.STATUS_CODES.get("SUCCESS", "Unavailable")
        else:
            catalog.status = catalog_processor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")

        catalog.save(db)
        db.commit()
        return
