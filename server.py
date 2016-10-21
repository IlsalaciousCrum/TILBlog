"""TIL Blog"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

from Model import (connect_to_db, db)

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['APP_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#  ---------------------------


#  ----------

if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    app.debug = True

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
