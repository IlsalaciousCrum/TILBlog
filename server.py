"""TIL Blog"""

from datetime import datetime

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from Model import (connect_to_db, db, User, Role)

import pytz

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['APP_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# to handle schema migration
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#  ---------------------------

# Views
@app.route('/')
def home():
    return render_template('index.html')

#  ----------


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    app.debug = True

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    manager.run()

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
