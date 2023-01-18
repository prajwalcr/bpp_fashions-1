from flask import render_template, request
from flaskapp import app, db
from werkzeug.utils import secure_filename
from flaskapp.utils import allowed_file
from flask_api import status
import os
from flaskapp.catalog_processor import *

CATALOG_PROCESSORS = {
    "json": JsonCatalogProcessor,
}
ALLOWED_FILES = set(CATALOG_PROCESSORS.keys())

@app.route('/ingest/<string:ingestionKey>', methods=["POST"])
def ingest(ingestionKey):
    if ingestionKey != app.config['INGESTION_KEY']:
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