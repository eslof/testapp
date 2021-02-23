import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, send_from_directory
from flask_restplus import Api
import os
import os.path

# region fixes serving of swagger interface files from -mzipapp .pyz
root_path = os.path.dirname(os.path.realpath(__file__))
if os.path.splitext(root_path)[1] == ".pyz":
    root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
template_folder = os.path.join(root_path, "templates")

app = Flask(__name__, template_folder=template_folder)


@app.route('/swaggerui/<path:filename>')
def file(filename):
    return send_from_directory(os.path.join(template_folder, "swaggerui"), filename)
# endregion


app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app)


