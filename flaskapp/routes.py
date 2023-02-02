from flask import render_template, jsonify, request
from flask_smorest import Blueprint
import requests
from flaskapp.cache import cache

blp = Blueprint("routes", __name__, description="Routes for HTML pages")


@blp.route('/')
def index():
    return render_template('search.html')



@blp.route('/productinfo/<string:id>')
def info(id):
    return render_template('product.html')


@blp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@blp.route("/search")
@cache.cached(timeout=30, query_string=True)
def get_search():

    query = request.args.get("q")
    params = {"q": query}
    response = requests.get("https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search", params = params)

    return jsonify(response.json())


