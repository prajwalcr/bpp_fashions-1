from flask import render_template, request
from flaskapp import app, db

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