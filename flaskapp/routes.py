from flask import render_template, request, jsonify
from flaskapp import app
from werkzeug.utils import secure_filename
from flaskapp.utils import allowed_file, validate_ingestion_key
from flask_api import status
import os
from flaskapp.catalog_processor import *
import uuid
from flaskapp.models import Catalog

CATALOG_PROCESSORS = {
    "json": JsonCatalogProcessor,
}
ALLOWED_FILES = set(CATALOG_PROCESSORS.keys())

db = SessionLocal()

def ingest_catalog(id):
    catalog = db.query(Catalog).filter_by(id=id).first()

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

@app.route('/upload-catalog/<string:ingestionKey>', methods=["POST"])
def upload_catalog(ingestionKey):
    if not validate_ingestion_key(ingestionKey):
        return "Invalid Ingestion Key", status.HTTP_401_UNAUTHORIZED
    if request.method == "POST":
        if "file" not in request.files:
            return "No File Selected", status.HTTP_400_BAD_REQUEST

        file = request.files["file"]
        if file and file.filename == '':
            return "No File Selected", status.HTTP_400_BAD_REQUEST

        if allowed_file(file.filename, ALLOWED_FILES):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            ext = filename.rsplit('.', 1)[1].lower()
            file.save(filepath)

            trackingID = str(uuid.uuid4())

            catalog = Catalog(id=trackingID, status="Validating Catalog", filepath=filepath)
            db.add(catalog)
            db.commit()

            response = {
                "message": "File Uploaded Successfully",
                "tracking ID": trackingID
            }

            ingest_catalog(trackingID)

            return jsonify(response), status.HTTP_200_OK

        return "Invalid File", status.HTTP_400_BAD_REQUEST

@app.route('/ingest/<string:ingestionKey>', methods=["POST"])
def ingest(ingestionKey):
    if not validate_ingestion_key(ingestionKey):
        return "Invalid Ingestion Key", status.HTTP_401_UNAUTHORIZED
    if request.method == "POST":
        if "file" not in request.files:
            return "No File Selected", status.HTTP_400_BAD_REQUEST

        file = request.files["file"]
        if file and file.filename == '':
            return "No File Selected", status.HTTP_400_BAD_REQUEST

        if allowed_file(file.filename, ALLOWED_FILES):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            ext = filename.rsplit('.', 1)[1].lower()
            file.save(filepath)

            catalogProcessor = CATALOG_PROCESSORS[ext](filepath)

            catalogProcessor.load()
            if not catalogProcessor.validate():
                return "Invalid File", status.HTTP_400_BAD_REQUEST

            if catalogProcessor.ingest():
                return "Successfully Uploaded Catalog", status.HTTP_200_OK
            else:
                return "Failed to Upload Catalog", status.HTTP_500_INTERNAL_SERVER_ERROR

    return "Invalid File", status.HTTP_400_BAD_REQUEST



@app.route('/')
def index():
    cat1 = request.args.get('cat1')
    cat2 = request.args.get('cat2')
    print(cat1, cat2)
    return render_template('search.html')


@app.route('/productinfo')
def info():
    return render_template('product.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404