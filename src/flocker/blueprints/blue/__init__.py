import os
from flask import Blueprint, render_template

def create_bp():
    bp_blue = Blueprint('blue', __name__, url_prefix='/blue')

    @bp_blue.route('/index/')
    @bp_blue.route('/')
    def index():
        return render_template('blue/index.html')
    
    return bp_blue