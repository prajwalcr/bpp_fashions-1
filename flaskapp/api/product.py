from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp import db
from sqlalchemy import func
from flaskapp.schemas import PlainProductSchema
from flaskapp.models import ProductModel, CategoryModel

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

        resp = []
        for product in products:
            productDict = {
                "id": product.ProductModel.id,
                "title": product.ProductModel.title,
                "availability": product.ProductModel.availability,
                "productDescription": product.ProductModel.productDescription,
                "imageURL": product.ProductModel.imageURL,
                "price": product.ProductModel.price
            }
            resp.append(productDict)

        return jsonify(resp)

@blp.route("/api/categories")
class Category(MethodView):
    def get(self):
        # Make the below code simpler
        # print(db.query(Category.catlevel1, func.group_concat(Category.catlevel2.distinct())).group_by(Category.catlevel1).all())
        sq = db.query(CategoryModel.catlevel1, CategoryModel.catlevel2).distinct().filter(CategoryModel.catlevel1 != None).subquery()
        catTree = db.query(sq.c.catlevel1, sq.c.catlevel2,
                           func.row_number().over(partition_by=sq.c.catlevel1).label("row_number")).all()

        resp = {}
        for item in catTree:
            if item[0] in resp:
                item[1] is None or resp[item[0]].append(item[1])
            else:
                resp[item[0]] = [item[1]] if item[1] is not None else []
        return jsonify(resp)