"""TIL Blog"""

# from datetime import datetime

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect

from Model import (connect_to_db, db, User, Post, PostCategories, Category)

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


# import pytz

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['APP_SECRET_KEY']

# raises an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

# handles schema migration
migrate = Migrate(app, db)

manager = Manager(app)
server = Server(host="0.0.0.0", port=5000, use_debugger=True, use_reloader=True)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

#  ---------------------------


@app.route('/')
def index():
    """Displays a homepage"""

    return render_template('index.html')


@app.route('/dashboard', methods=['POST'])
def show_dashboard():
    """A post sign-in page for authorized users"""


@app.route('/add', methods=['POST'])
def add_post():
    """Allows logged in users to add new posts"""


@app.route('/edit', methods=['POST'])
def edit_post():
    """Allows logged in users to edit existing posts"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Verifies the user and adds a session"""


@app.route('/logout')
def logout():
    """Clear's the session"""


# ___________________________________________________________________________


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # app.debug = True

    # DEBUG = "NO_DEBUG" not in os.environ

    # PORT = int(os.environ.get("PORT", 5000))

    # app.run(host="0.0.0.0", port=PORT, debug=DEBUG)

    manager.run()
