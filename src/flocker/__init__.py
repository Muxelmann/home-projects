import os
import importlib
import jinja2
from flask import Flask, render_template

def create_app():
    '''App creation factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(16)

    # sample_file_path = os.path.sep.join((app.instance_path, 'data.json'))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Tidy up all symbolically linked templates and statics
    templates = os.listdir(os.path.join(os.path.dirname(__file__), 'templates'))
    for f in templates:
        link_path = os.path.join(os.path.dirname(__file__), 'templates', f)
        if os.path.islink(link_path):
            os.remove(link_path)

    statics = os.listdir(os.path.join(os.path.dirname(__file__), 'static'))
    for f in statics:
        link_path = os.path.join(os.path.dirname(__file__), 'static', f)
        if os.path.islink(link_path):
            os.remove(link_path)

    # Find all blueprints
    blueprint_names = [b for b in os.listdir(os.path.join(os.path.dirname(__file__), 'blueprints')) if b[0] is not '.']
    blueprints = {}

    for blueprint_name in blueprint_names:
        # Import and register blueprints
        mod = importlib.import_module('flocker.blueprints.{}'.format(blueprint_name))
        blueprints[blueprint_name] = mod.create_bp()
        app.register_blueprint(blueprints[blueprint_name])

        # Also add their templates and statics as symlinks
        src_dir = os.path.join(os.path.dirname(__file__), 'blueprints', blueprint_name, 'templates')
        dst_dir = os.path.join(os.path.dirname(__file__), 'templates', blueprint_name)
        os.symlink(src_dir, dst_dir)

        src_dir = os.path.join(os.path.dirname(__file__), 'blueprints', blueprint_name, 'static')
        dst_dir = os.path.join(os.path.dirname(__file__), 'static', blueprint_name)
        os.symlink(src_dir, dst_dir)

    @app.route('/index/')
    @app.route('/')
    def index():
        return render_template('index.html', blueprints=blueprints.values())

    return app