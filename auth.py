from flask import Blueprint, render_template, abort, request, redirect
from flask.ext.login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import User, get_user, has_superuser, write_to_db
from settings import SECRET_KEY

auth = Blueprint('auth', __name__, template_folder='templates')

# Auth Helpers/Flask-Login
auth_sys = LoginManager()

def setup_auth(app):
    auth_sys.init_app(app)


# Use the UserMixin from Flask-Login to make this easy.
class FLUser(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.username

    # Redirect missing attributes to the User object
    def __getattr__(self, name):
        return self.user.__getattr__(name)


@auth_sys.user_loader
def load_user(uname):
    user = get_user(uname)
    if user:
        return FLUser(user)
    return None

@auth_sys.unauthorized_handler
def unauthorized():
    return redirect('/login')


def create_user(name, password, sudo=False):
    if not name or not password or len(name) < 3 or len(password) < 4:
        raise ValueError()
    u = User(username=name.lower(), password=generate_password_hash(password))
    u.is_superuser = sudo
    write_to_db(u)

def check_password(user, password):
    return check_password_hash(user.password, password)


# Flask Routing
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('auth/logout.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect('/')

    if not has_superuser():
        return redirect('/firstrun')

    errs = None
    if request.method == 'POST':
        try:
            print(request.form)
            uname = request.form['username'].lower()
            user = get_user(uname)
            assert user
            print(check_password(user, request.form['password']))
            assert check_password(user, request.form['password'])
            remember = False
            if 'remember' in request.form:
                remember = True
            login_user(FLUser(user))
            return redirect('/')
        except Exception as ex:
            print(ex)
            errs = ["Incorrect username/password."]

    return render_template('auth/login.html', errors=errs)

@auth.route('/firstrun', methods=['GET', 'POST'])
def firstrun():
    if has_superuser():
        return redirect('/login')

    errs = None
    if request.method == 'POST':
        try:
            assert request.form['password'] == request.form['password-confirm']
            uname = request.form['username'].lower()
            create_user(request.form['username'], request.form['password'], sudo=True)
            return render_template('auth/setup_complete.html')
        except Exception as ex:
            errs = ["Invalid credentials. Mismatching passwords?"]

    return render_template('auth/firstrun.html', errors=errs)
