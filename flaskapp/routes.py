from flask import render_template, request, jsonify
from flask_smorest import Blueprint
import requests

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


