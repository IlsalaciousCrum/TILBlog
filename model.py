"""Models for TIL Blog"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

##############################################################################
# Model definitions


class Post(db.Model):
    """A blog entry"""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(128), nullable=False, unique=True)
    subject = db.Column(db.String(128), nullable=False, unique=False)
    body = db.Column(db.Text)

    categories = db.relationship("Category",
                                 secondary="postcategories",
                                 backref="posts")


class PostCategories(db.Model):
    """An association table to let a post have multiple categories"""

    __tablename__ = "postcategories"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'), nullable=False)


class Category(db.Model):
    """Topical category for blog post"""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(120), nullable=False, unique=True)
    category_description = db.Column(db.String(250), nullable=True)

    posts = db.relationship("Post",
                            secondary="postcategories",
                            backref="posts")


# def example_data():
# """Create some sample data."""

#   df = Dept(dept_code='fin', dept='Finance', phone='555-1000')
#   dl = Dept(dept_code='legal', dept='Legal', phone='555-2222')
#   dm = Dept(dept_code='mktg', dept='Marketing', phone='555-9999')

#   leonard = Employee(name='Leonard', dept=dl)
#   liz = Employee(name='Liz', dept=dl)
#   maggie = Employee(name='Maggie', dept=dm)
#   nadine = Employee(name='Nadine')

#   db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
#   db.session.commit()


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
