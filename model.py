"""Models for TIL Blog"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

##############################################################################
# Model definitions

class Post(db.Model):
    """A blog entry"""

    __tablename__ = "players"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timestamp = db.Column(db.DateTime)



class Category(db.Model):
    """Topical category for blog post"""

    __tablename__ = "categories"

    






##############################################################################
# Database Helper functions

def connect_to_db(app, db_uri=None):
    '''Connect the database to Flask app.'''

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///blog'
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    migrate = Migrate(app, db)
    print 'Connected to DB.'
