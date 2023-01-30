from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp import db
from sqlalchemy import func
from flaskapp.schemas import PlainProductSchema, SearchSchema, ProductListSchema, PaginationSchema, \
    ProductParameterSchema
from flaskapp.models import ProductModel, CategoryModel

import requests


blp = Blueprint("product", __name__, description="Operations on products")

def fireSearchQuery(searchParams):
    searchURL = current_app.config['UNBXD_SEARCH_URL'] + current_app.config['UNBXD_API_KEY'] \
                + "/" + current_app.config['SITE_KEY'] + "/search/"

    requiredFields = ["uniqueId", "title", "availability", "productDescription", "productImage", "price"]

    searchParams["fields"] = ",".join(requiredFields)
    searchData = requests.get(searchURL, params=searchParams).json()

    return searchData
def getSearchResponse(searchParams):

    searchData = fireSearchQuery(searchParams)

    if "response" not in searchData or "products" not in searchData["response"] or "numberOfProducts" not in searchData[
        "response"]:
        return 500, "Search API Down"

    numberOfProducts = searchData["response"]["numberOfProducts"]

    productList = []

    for dataItem in searchData["response"]["products"]:
        if "uniqueId" not in dataItem or "price" not in dataItem:
            numberOfProducts -= 1
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

        productList.append(product)

    return 200, {
        "products": productList,
        "total": numberOfProducts
    }

@blp.route("/api/products/<string:product_id>")
class Product(MethodView):
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        q = db.query(ProductModel).filter_by(id=product_id)
        if not db.query(q.exists()).scalar():
            print("No exist")
            searchParams = {
                "q": product_id
            }
            status, response = getSearchResponse(searchParams)

            if status != 200:
                abort(status, message=response)

            if response["total"] < 1:
                abort(404, message="Resource not found")

            return response["products"][0]

        product = q.first()

        return product

@blp.route("/api/products")
class ProductList(MethodView):
    @blp.arguments(ProductParameterSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, productParameters):
        q = db.query(ProductModel, CategoryModel).filter(ProductModel.id == CategoryModel.product_id)

        if "cat1" in productParameters:
            q = q.filter(CategoryModel.catlevel1 == productParameters["cat1"])
        if "cat2" in productParameters:
            q = q.filter(CategoryModel.catlevel2 == productParameters["cat2"])

        if "sort" in productParameters and productParameters["sort"].lower().split()[0] == "price":
            sortOrder = productParameters["sort"].lower().split()[-1]

            if sortOrder == "desc":
                q = q.order_by(ProductModel.price.desc())
            else:
                q = q.order_by(ProductModel.price.asc())

        rows = productParameters.get("rows", current_app.config["PRODUCTS_PER_PAGE"])
        products = q.limit(rows).offset((productParameters.get("page", 1)-1)*rows).all()

        total = q.count()

        response = {
            "total": total,
            "products": [product["ProductModel"] for product in products]
        }

        return response

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
    @blp.arguments(SearchSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, searchParams):
        status, response = getSearchResponse(searchParams)

        if status != 200:
            abort(status, message=response)

        return response


