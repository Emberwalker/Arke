from flask import Blueprint, render_template, abort, request

core = Blueprint('core', __name__, template_folder='templates')

