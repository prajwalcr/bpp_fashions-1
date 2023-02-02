from flask import render_template
from flask_smorest import Blueprint

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
