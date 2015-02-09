from flask import Blueprint, render_template, abort, request, redirect

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    if True: # TODO: Run this only on first run.
        return redirect('/firstrun')

    errs = None
    if request.method == 'POST':
        pass # TODO: Auth.

    return render_template('auth/login.html', errors=errs)

@auth.route('/firstrun')
def firstrun():
    errs = None
    if request.method == 'POST':
        pass # TODO: Create superuser

    return render_template('auth/firstrun.html', errors=errs)
