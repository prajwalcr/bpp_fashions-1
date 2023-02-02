from flask import current_app


def get_file_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1]


def validate_site_key(site_key):
    return site_key == current_app.config['SITE_KEY']


def pagination_page_limit(rows, total):
    return ((total - 1) // rows) + 1
