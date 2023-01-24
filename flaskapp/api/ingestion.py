from flask import request, jsonify, current_app
from flask.views import MethodView
from flaskapp.database import SessionLocal
from flask_smorest import Blueprint, abort

from flaskapp.models import CatalogModel
from flaskapp.utils import allowed_file, validate_ingestion_key
from werkzeug.utils import secure_filename
from flaskapp.CatalogProcessor import JsonCatalogProcessor

from threading import Thread
import uuid
import os

db = SessionLocal()
blp = Blueprint("ingestion", __name__, description="Ingest catalog into system")

CATALOG_PROCESSORS = {
    "json": JsonCatalogProcessor,
}
ALLOWED_FILES = set(CATALOG_PROCESSORS.keys())

@blp.route("/api/upload-catalog/<string:ingestionKey>")
class IngestCatalog(MethodView):
    def ingest_catalog(self, id):
        catalog = db.query(CatalogModel).filter_by(id=id).first()

        filepath = catalog.filepath
        ext = filepath.rsplit('.', 1)[1].lower()

        catalogProcessor = CATALOG_PROCESSORS[ext](filepath)

        catalogProcessor.load()
        if not catalogProcessor.validate():
            catalog.status = "Validation Failed"
            db.commit()
            return

        catalog.status = "Ingesting Catalog"
        db.commit()

        if catalogProcessor.ingest():
            catalog.status = "Successfully Ingested Catalog"
        else:
            catalog.status = "Catalog Ingestion Failed"

        db.commit()
        return

    def post(self, ingestionKey):
        if not validate_ingestion_key(ingestionKey):
            abort(401, message="Invalid Ingestion Key")
        if request.method == "POST":
            if "file" not in request.files:
                abort(400, message="No File Selected")

            file = request.files["file"]
            if file and file.filename == '':
                abort(400, message="No File Selected")

            if allowed_file(file.filename, ALLOWED_FILES):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                trackingID = str(uuid.uuid4().hex)

                catalog = CatalogModel(id=trackingID, status="Validating Catalog", filepath=filepath)
                print("added catalog")
                db.add(catalog)
                db.commit()

                response = {
                    "message": "File Uploaded Successfully",
                    "tracking ID": trackingID
                }

                Thread(target=self.ingest_catalog, args=(trackingID,)).start()

                return jsonify(response)

            return abort(400, message="Invalid File")