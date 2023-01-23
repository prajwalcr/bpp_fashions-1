from flask import render_template, request, jsonify, abort
from flaskapp import app, SessionLocal

from werkzeug.utils import secure_filename
from flaskapp.utils import allowed_file, validate_ingestion_key
from flask_api import status
import os
from flaskapp.catalog_processor import JsonCatalogProcessor
import uuid
from flaskapp.models import Catalog, Product, Category

from threading import Thread
from sqlalchemy import func, desc

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
            file.save(filepath)

            trackingID = str(uuid.uuid4())

            catalog = Catalog(id=trackingID, status="Validating Catalog", filepath=filepath)
            db.add(catalog)
            db.commit()

            response = {
                "message": "File Uploaded Successfully",
                "tracking ID": trackingID
            }

            Thread(target=ingest_catalog, args=(trackingID,)).start()

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


@app.route('/product/<string:id>')
def get_product(id):
    q = db.query(Product).filter_by(id=id)
    if not db.query(q.exists()).scalar():
        abort(404, description="Resource not found")

    product = q.first()
    resp = {
        "id": product.id,
        "title": product.title,
        "availability": product.availability,
        "productDescription": product.productDescription,
        "imageURL": product.imageURL,
        "price": product.price
    }
    return jsonify(resp)

@app.route('/products')  # /products?cat1=dfjslk&cat2=dfasljk
def get_products():
    cat1 = request.args.get("cat1")
    cat2 = request.args.get("cat2")

    q = db.query(Product)
    if cat1 is not None:
        q = q.filter_by(parent_category=cat1)
    if cat2 is not None:
        q = q.filter_by(category_name=cat2)

    products = q.all()

    resp = []
    for product in products:
        productDict = {
            "id": product.id,
            "title": product.title,
            "availability": product.availability,
            "productDescription": product.productDescription,
            "imageURL": product.imageURL,
            "price": product.price
        }
        resp.append(productDict)

    return jsonify(resp)

@app.route('/categories')
def categories():

    # Make the below code simpler
    # print(db.query(Category.catlevel1, func.group_concat(Category.catlevel2.distinct())).group_by(Category.catlevel1).all())
    sq = db.query(Category.catlevel1, Category.catlevel2).distinct().filter(Category.catlevel1!=None).subquery()
    catTree = db.query(sq.c.catlevel1, sq.c.catlevel2, func.row_number().over(partition_by=sq.c.catlevel1).label("row_number")).all()

    resp = {}
    for item in catTree:
        if item[0] in resp:
            item[1] is None or resp[item[0]].append(item[1])
        else:
            resp[item[0]] = [item[1]] if item[1] is not None else []
    return jsonify(resp)

@app.route('/')
def index():
    cat1 = request.args.get('cat1')
    cat2 = request.args.get('cat2')
    print(cat1, cat2)
    return render_template('search.html')


@app.route('/productinfo/<string:id>')
def info(id):
    return render_template('product.html')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404