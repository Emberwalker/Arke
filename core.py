from flask import Blueprint, render_template, abort, request
from flask.ext.login import login_required
from db import get_all, Category

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
@login_required
def index():
    return render_template('core/index.html', categories=get_all(Category))

@core.route('/create-vote')
@login_required
def create_vote():
    return render_template('core/create_vote.html')
