from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import User, get_user, has_superuser, write_to_db, delete_from_db, get_all
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
        return getattr(self.user, name)


@auth_sys.user_loader
def load_user(uname):
    user = get_user(uname)
    if user:
        return FLUser(user)
    return None

@auth_sys.unauthorized_handler
def unauthorized():
    return redirect('/login')


class UserExists(ValueError):
    pass

class NoPermissionError(Exception):
    pass

def create_user(name, password, sudo=False):
    if not name or not password or len(name) < 3 or len(password) < 4 or name.isdigit():  # Disallow unames that are numbers to avoid confusing the ID catcher
        raise ValueError()
    if get_user(name.lower()):
        raise UserExists()
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
            uname = request.form['username'].lower()
            user = get_user(uname)
            assert user
            assert check_password(user, request.form['password'])
            remember = False
            if 'remember' in request.form:
                remember = True
            login_user(FLUser(user))
            return redirect('/')
        except Exception as ex:
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
            create_user(uname, request.form['password'], sudo=True)
            return render_template('auth/setup_complete.html')
        except Exception as ex:
            errs = ["Invalid credentials. Mismatching passwords?"]

    return render_template('auth/firstrun.html', errors=errs)


ERR_USER_EXISTS = "User already exists; perhaps you wanted <a href=\"/manage-accounts\">account management</a>?"

@auth.route('/create-user', methods=['GET', 'POST'])
@login_required
def create_user_page():
    if not current_user.is_superuser:
        return redirect('/')

    errs = None
    info = None
    if request.method == 'POST':
        try:
            assert request.form['password'] == request.form['password-confirm']
            uname = request.form['username']
            admin = True if 'superuser' in request.form else False
            create_user(uname, request.form['password'], sudo=admin)
            info = "User '{}' created.".format(uname)
        except UserExists:
            errs = [ERR_USER_EXISTS]
        except Exception as ex:
            errs = ["User creation failed; mismatching passwords?"]

    return render_template('auth/create_user.html', errors=errs, info=info)

@auth.route('/manage-accounts')
@login_required
def manage_accounts():
    if not current_user.is_superuser:
        return redirect('/')

    info = request.args.get('info', None)
    errs = []

    return render_template('auth/manage.html', users=get_all(User), errors=errs, info=info)

@auth.route('/users/destroy', methods=['GET', 'POST'])
@login_required
def destroy_user():
    if not current_user.is_superuser:
        return redirect('/')

    uid = request.args.get('uid', None)
    if not uid:
        return redirect(url_for('auth.manage_accounts'))

    user = get_user(uid)
    errs = None

    if not user:
        return redirect(url_for('auth.manage_accounts'))

    if request.method == 'POST':
        # Actually destroy
        uname = user.username
        try:
            delete_from_db(user)
            return redirect(url_for('auth.manage_accounts', info="User {} deleted.".format(uname)))
        except Exception as ex:
            errs = [str(ex)]

    return render_template('auth/destroy.html', user=user, errors=errs)

@auth.route('/users/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    uid = request.args.get('uid', None)
    user = None
    if uid and current_user.is_superuser:
        user = get_user(uid)
    else:
        user = current_user

    errs = None
    info = None

    if request.method == 'POST':
        try:
            uname = request.form['username']
            pw1 = request.form['password']
            pw2 = request.form['password-confirm']
            assert pw1 == pw2
            if not uname == current_user.username and not current_user.is_superuser:
                raise NoPermissionError()
            u = get_user(uname)
            if len(pw1) < 4:
                raise ValueError()
            u.password = generate_password_hash(pw1)
            write_to_db(u)
            info = "Password changed for '{}'".format(uname)
        except NoPermissionError:
            errs = ["Permission denied."]
        except Exception as ex:
            print(ex)
            errs = ["Password change failed; mismatching passwords?"]

    return render_template('auth/change_password.html', user=user, errors=errs, info=info)

