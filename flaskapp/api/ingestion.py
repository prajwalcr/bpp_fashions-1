from flask import request, jsonify, current_app
from flask.views import MethodView
from flaskapp.database import SessionLocal
from flask_smorest import Blueprint, abort

from flaskapp.models import CatalogModel
from flaskapp.utils import allowed_file, validate_site_key
from werkzeug.utils import secure_filename
from flaskapp.CatalogProcessors.CatalogProcessor import CatalogProcessor
from flaskapp.CatalogProcessors.JsonCatalogProcessor import JsonCatalogProcessor
from flaskapp.schemas import MultiPartFileSchema

from threading import Thread
import uuid
import os

db = SessionLocal()
blp = Blueprint("ingestion", __name__, description="Ingest catalog into system")

CATALOG_PROCESSORS = {
    "json": JsonCatalogProcessor,
}
ALLOWED_FILES = set(CATALOG_PROCESSORS.keys())

@blp.route("/api/upload-catalog/<string:siteKey>")
class IngestCatalog(MethodView):
    def exception_handler(func):
        from functools import wraps
        @wraps(func)
        def inner_function(self, id, *args, **kwargs):
            try:
                return func(self, id, *args, **kwargs)
            except Exception as e:
                print(f"Exception in {func.__name__}:", e)

                catalog = db.query(CatalogModel).filter_by(id=id).first()
                catalog.status = CatalogProcessor.STATUS_CODES.get("INGESTION_FAILURE", "Unavailable")
                db.commit()

        return inner_function

    @exception_handler
    def ingest_catalog(self, id):
        catalog = db.query(CatalogModel).filter_by(id=id).first()

        filepath = catalog.filepath
        ext = filepath.rsplit('.', 1)[1].lower()

        catalogProcessor = CATALOG_PROCESSORS[ext](filepath)

        catalogProcessor.load()
        if not catalogProcessor.validate():
            catalog.status = catalogProcessor.STATUS_CODE.get("VALIDATION_FAILURE", "Unavailable")
            db.commit()
            return

        catalog.status = catalogProcessor.STATUS_CODE.get("INGESTING", "Unavailable")
        db.commit()

        if catalogProcessor.ingest():
            catalog.status = catalogProcessor.STATUS_CODE.get("SUCCESS", "Unavailable")
        else:
            catalog.status = catalogProcessor.STATUS_CODE.get("INGESTION_FAILURE", "Unavailable")

        db.commit()
        return

    @blp.arguments(MultiPartFileSchema, location="files")
    @blp.response(201)
    def post(self, files, siteKey):
        if not validate_site_key(siteKey):
            abort(401, message="Invalid Ingestion Key")
        if request.method == "POST":
            if "file" not in files:
                abort(400, message="No File Selected")

            file = files["file"]
            if file and file.filename == '':
                abort(400, message="No File Selected")

            if allowed_file(file.filename, ALLOWED_FILES):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                trackingID = str(uuid.uuid4().hex)

                catalog = CatalogModel(id=trackingID, status=CatalogProcessor.STATUS_CODES.get("VALIDATING", "Unavailable"), filepath=filepath)
                print("added catalog")
                db.add(catalog)
                db.commit()

                response = {
                    "message": "File Uploaded Successfully",
                    "tracking ID": trackingID
                }

                try:
                    Thread(target=self.ingest_catalog, args=(trackingID,)).start()
                except Exception as e:
                    print("Exception in ingestion:", e)

                return jsonify(response)

            return abort(400, message="Invalid File")