import os
from flask import Blueprint, render_template

def create_bp():
    bp_red = Blueprint('red', __name__, url_prefix='/red')

    @bp_red.route('/index/')
    @bp_red.route('/')
    def index():
        return render_template('red/index.html')
    
    return bp_red