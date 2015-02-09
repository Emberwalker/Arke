from flask import Blueprint, render_template, abort, request
from flask.ext.login import login_required

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
@login_required
def index():
    return render_template('core/index.html')
