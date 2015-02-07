from flask import Flask
import os

from auth import auth
from core import core

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(core)

# Runtime
if __name__ == '__main__':
    try:
        dbg = os.environ["DEBUG"]
        app.debug = True
        app.run(host='0.0.0.0', port=8080)
    except KeyError:
        app.run(port=8080)
