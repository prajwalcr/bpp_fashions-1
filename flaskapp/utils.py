from flask import current_app
def allowed_file(filename, allowedExtensions=None):
    # if allowedExtensions is None:
    #     return '.' in filename
    return '.' in filename and (allowedExtensions is None or filename.rsplit('.', 1)[1].lower() in allowedExtensions)

def validate_site_key(siteKey):
    return siteKey == current_app.config['SITE_KEY']

