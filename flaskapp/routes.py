from flask import render_template, request, jsonify
from flask_smorest import Blueprint
import requests

blp = Blueprint("routes", __name__, description="Routes for HTML pages")

@blp.route('/')
def index():
    cat1 = request.args.get('cat1')
    cat2 = request.args.get('cat2')
    print(cat1, cat2)
    return render_template('search.html')


@blp.route('/productinfo/<string:id>')
def info(id):
    return render_template('product.html')


@blp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

"search?q=shirt"
@blp.route("/search")
def get_search():

    query = request.args.get("q")
    params = {"q": query}
    response = requests.get("https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search", params = params)

    print(response.json())
    return jsonify(response.json())

