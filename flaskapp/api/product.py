from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp import db
from sqlalchemy import func
from flaskapp.schemas import PlainProductSchema, ProductSearchSchema, ProductPaginationSchema
from flaskapp.models import ProductModel, CategoryModel

import requests

blp = Blueprint("product", __name__, description="Operations on products")

@blp.route("/api/products/<string:product_id>")
class Product(MethodView):
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        q = db.query(ProductModel).filter_by(id=product_id)
        if not db.query(q.exists()).scalar():
            abort(404, message="Resource not found")

        product = q.first()

        return product

@blp.route("/api/products")
class ProductList(MethodView):
    @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        cat1 = request.args.get("cat1")
        cat2 = request.args.get("cat2")

        q = db.query(ProductModel, CategoryModel).filter(ProductModel.id == CategoryModel.product_id)

        if cat1 is not None:
            q = q.filter(CategoryModel.catlevel1 == cat1)
        if cat2 is not None:
            q = q.filter(CategoryModel.catlevel2 == cat2)

        products = q.all()

        return [product["ProductModel"] for product in products]

@blp.route("/api/categories")
class Category(MethodView):
    def get(self):
        # Make the below code simpler
        # print(db.query(Category.catlevel1, func.group_concat(Category.catlevel2.distinct())).group_by(Category.catlevel1).all())
        categoryQuery = db.query(CategoryModel.catlevel1, CategoryModel.catlevel2).distinct().filter(CategoryModel.catlevel1 != None).subquery()
        categoryTree = db.query(categoryQuery.c.catlevel1, categoryQuery.c.catlevel2,
                           func.row_number().over(partition_by=categoryQuery.c.catlevel1).label("row_number")).all()

        resp = {}
        for item in categoryTree:
            if item[0] in resp:
                item[1] is None or resp[item[0]].append(item[1])
            else:
                resp[item[0]] = [item[1]] if item[1] is not None else []
        return jsonify(resp)


@blp.route("/api/search")
class ProductSearch(MethodView):
    @blp.arguments(ProductSearchSchema, location="query")
    @blp.response(200, ProductPaginationSchema)
    def get(self, searchParams):

        searchURL = current_app.config['UNBXD_SEARCH_URL'] + current_app.config['UNBXD_API_KEY'] \
                    + "/" + current_app.config['SITE_KEY'] + "/search/"

        searchData = requests.get(searchURL, params=searchParams).json()

        if "response" not in searchData or "products" not in searchData["response"] or "numberOfProducts" not in searchData["response"]:
            abort(500, message="Search API Down")

        numberOfProducts = searchData["response"]["numberOfProducts"]

        response = {
            "total": numberOfProducts,
            "products": []
        }

        for dataItem in searchData["response"]["products"]:
            if "uniqueId" not in dataItem or "price" not in dataItem:
                continue

            id = dataItem["uniqueId"]
            title = dataItem.get("title", None)

            if "availability" in dataItem:
                availability = dataItem["availability"].lower() == "true"
            else:
                availability = False

            productDescription = dataItem.get("productDescription", None)
            imageURL = dataItem.get("productImage", None)  # Replace this maybe
            price = dataItem["price"]

            product = ProductModel(
                id=id,
                title=title,
                availability=availability,
                productDescription=productDescription,
                imageURL=imageURL,
                price=price
            )

            response["products"].append(product)
            print(response)
        return response



