"""Models for TIL Blog"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from helper_functions import encrypt, random_string


db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """An admin user of the blog"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    session_code = db.Column(db.String(25), nullable=False, unique=False)
    email = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(200), nullable=False)


class Post(db.Model):
    """A blog entry"""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(128), nullable=False, unique=True)
    subject = db.Column(db.String(128), nullable=False, unique=False)
    body = db.Column(db.Text)


class PostCategories(db.Model):
    """An association table to let a post have multiple categories"""

    __tablename__ = "postcategories"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'), nullable=False)

    posts = db.relationship("Post", backref="postcategories")
    categories = db.relationship("Category", backref="postcategories")


class Category(db.Model):
    """Topical category for blog post"""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(120), nullable=False, unique=True)
    category_description = db.Column(db.String(250), nullable=True)


def example_data():
    """Create some sample data."""

    username = encrypt('George')
    password = encrypt('fXgbAk/3pKZmPHMGgN*kd8v{7Hy')
    session_code = random_string()
    hashed_session_code = encrypt(session_code)
    email = encrypt('loislane@gmail.com')
    phone_number = encrypt('555-122-1212')

    fake_user = User(username=username, password=password,
                     session_code=hashed_session_code, email=email, phone_number=phone_number)

    a1 = "21-Oct-2016 14:25:01.426226"
    a2 = "08-Oct-1976 07:25:01.426226"
    a3 = "23-Apr-2015 20:25:01.426226"

    local = pytz.timezone("US/Pacific")

    b1 = datetime.strptime(a1, "%d-%b-%Y %H:%M:%S.%f")
    b2 = datetime.strptime(a2, "%d-%b-%Y %H:%M:%S.%f")
    b3 = datetime.strptime(a3, "%d-%b-%Y %H:%M:%S.%f")

    c1 = local.localize(b1, is_dst=None)
    c2 = local.localize(b2, is_dst=None)
    c3 = local.localize(b3, is_dst=None)

    A = Post(post_id=c1, timestamp='2016-10-01 12:18:36.401789-07:00', title='Lorem I', subject='Lorem ipsum dolor sit amet, vidisse offendit ea vix, elit falli scribentur cu vix.', body='<p>Lorem ipsum dolor sit amet, vidisse offendit ea vix, elit falli scribentur cu vix. Vel ex possim vituperata, ex sed prima posidonium persequeris. Pri no atqui debitis, autem reprimique ea duo. Malorum iuvaret voluptua nam et, te usu putant prompta scribentur. Pri ea noluisse oporteat senserit, eum ne saepe appareat patrioque, mel at dolor consequat. Ut quo porro laudem, vero scripserit efficiantur an nam, nibh pericula id vim.</p><p>Mei graecis pertinacia no. Cu vel oratio eleifend scribentur. Has cu dicam legendos accommodare, his tota nonumy id. Usu labore interesset mediocritatem et, id posse dissentias vel. Legendos volutpat similique ea sit. Eligendi delicata concludaturque nec cu, et nec platonem ullamcorper.</p><p>Graeci timeam recusabo ut eum. Quem oportere ea pri, sit ex semper splendide tincidunt. Has an legimus legendos imperdiet. Pertinacia maiestatis eum eu. Mei ut iracundia urbanitas, pro semper diceret ad.</p><p>Meis delenit constituto in his, sea melius delenit in. Ad eum wisi vocibus senserit, est ne sint instructior. Vel ei tacimates forensibus incorrupte. Et nam quod dignissim. Vis nulla animal utamur ad, te vix semper feugait patrioque.</p><p>Cum accusam oportere ocurreret ex. Aperiam iuvaret theophrastus pro te. Illud justo vocibus an quo. Et sit oratio mnesarchum reformidans, agam modus feugiat eum ea. Ad ius aperiri erroribus omittantur. An nullam officiis sit.</p>')
    B = Post(post_id=c2, timestamp='2016-07-01 12:18:36.401789-07:00', body='No, I\'m Santa Claus! I\'m a thing. Fetal stemcells, aren\'t those controversial? Oh, you\'re a dollar naughtier than most. We don\'t have a brig.')
    C = Post(post_id=c3, timestamp='2016-06-01 12:18:36.401789-07:00', title='Where does it come from?', subject='You hate me; you want to kill me! Well, go on! Kill me! KILL ME! Father Christmas. Santa Claus. Or as I\'ve always known him: Jeff. I\'m the Doctor, I\'m worse than everyone\'s aunt. *catches himself* And that is not how I\'m introducing myself.', body='<p>Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.</p><p>The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham. </p>')

    D = Category(category_name='Whiteboarding', category_description='About preparing for whiteboarding challenges')
    E = Category(category_name='Code challenge', category_description='About preparing for take home or timed coding challenges')
    F = Category(category_name='Making things', category_description='About learning new technologies to make things with code')

    G = PostCategories(post_id=1, cat_id=1)
    H = PostCategories(post_id=3, cat_id=2)
    I = PostCategories(post_id=3, cat_id=3)
    J = PostCategories(post_id=2, cat_id=2)
    K = PostCategories(post_id=2, cat_id=3)

    db.session.add_all([A, B, C, D, E, F, G, H, I, J, K, fake_user])
    db.session.commit()

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

##############################################################################

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
