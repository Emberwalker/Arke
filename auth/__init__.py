from flask import Blueprint, render_template, abort, request

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    errs = None
    if request.method == 'POST':
        pass # TODO: Auth.

    return render_template('auth/login.html', errors=errs)
