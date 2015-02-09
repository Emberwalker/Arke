import os
try:
    dbg = os.environ['DEBUG']
    DEBUG = True
except KeyError:
    DEBUG = False

from flask import Flask
from settings import DB_URL
from auth import auth
from core import core

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(core)

# Runtime
if __name__ == '__main__':
    if DEBUG:
        DB_URL = "sqlite:///development.db"
        app.debug = True
        app.run(host='0.0.0.0', port=8080)
    else:
        app.run(port=8080)
