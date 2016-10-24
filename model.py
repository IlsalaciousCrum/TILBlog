"""Models for TIL Blog"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from datetime import datetime
import pytz

db = SQLAlchemy()

##############################################################################
# Model definitions

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='ilsalacious@gmail.com', password='password123')
    db.session.commit()



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


def example_data():
    """Create some sample data."""

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
    C = Post(post_id=c3, timestamp='2016-06-01 12:18:36.401789-07:00', title='Heh-haa! Super squeaky bum time!', subject='You hate me; you want to kill me! Well, go on! Kill me! KILL ME! Father Christmas. Santa Claus. Or as I\'ve always known him: Jeff. I\'m the Doctor, I\'m worse than everyone\'s aunt. *catches himself* And that is not how I\'m introducing myself.', body='<p>No, I\'ll fix it. I\'m good at fixing rot. Call me the Rotmeister. No, I\'m the Doctor. Don\'t call me the Rotmeister. They\'re not aliens, they\'re Earth…liens! Father Christmas. Santa Claus. Or as I\'ve always known him: Jeff. Saving the world with meals on wheels. Aw, you\'re all Mr. Grumpy Face today. I hate yogurt. It\'s just stuff with bits in. *Insistently* Bow ties are cool! Come on Amy, I\'m a normal bloke, tell me what normal blokes do!</p><p>I\'m nobody\'s taxi service; I\'m not gonna be there to catch you every time you feel like jumping out of a spaceship. I am the last of my species, and I know how that weighs on the heart so don\'t lie to me!</p><p>Stop talking, brain thinking. Hush. You know when grown-ups tell you \'everything\'s going to be fine\' and you think they\'re probably lying to make you feel better? They\'re not aliens, they\'re Earth…liens!</p><p>I\'m the Doctor. Well, they call me the Doctor. I don\'t know why. I call me the Doctor too. I still don\'t know why. Annihilate? No. No violence. I won\'t stand for it. Not now, not ever, do you understand me?! I\'m the Doctor, the Oncoming Storm - and you basically meant beat them in a football match, didn\'t you?</p><p>You know when grown-ups tell you \'everything\'s going to be fine\' and you think they\'re probably lying to make you feel better? You know when grown-ups tell you \'everything\'s going to be fine\' and you think they\'re probably lying to make you feel better?</p><p>Sorry, checking all the water in this area; there\'s an escaped fish. It\'s a fez. I wear a fez now. Fezes are cool. The way I see it, every life is a pile of good things and bad things.…hey.…the good things don\'t always soften the bad things; but vice-versa the bad things don\'t necessarily spoil the good things and make them unimportant.</p><p>No, I\'ll fix it. I\'m good at fixing rot. Call me the Rotmeister. No, I\'m the Doctor. Don\'t call me the Rotmeister. You hit me with a cricket bat. You hit me with a cricket bat. You\'ve swallowed a planet!</p><P>I\'m the Doctor, I\'m worse than everyone\'s aunt. *catches himself* And that is not how I\'m introducing myself. I\'m the Doctor. Well, they call me the Doctor. I don\'t know why. I call me the Doctor too. I still don\'t know why.</p><P>You know when grown-ups tell you \'everything\'s going to be fine\' and you think they\'re probably lying to make you feel better? It\'s a fez. I wear a fez now. Fezes are cool. No, I\'ll fix it. I\'m good at fixing rot. Call me the Rotmeister. No, I\'m the Doctor. Don\'t call me the Rotmeister.</p><p>No… It\'s a thing; it\'s like a plan, but with more greatness. I\'m nobody\'s taxi service; I\'m not gonna be there to catch you every time you feel like jumping out of a spaceship. *Insistently* Bow ties are cool! Come on Amy, I\'m a normal bloke, tell me what normal blokes do!</p><p>Annihilate? No. No violence. I won\'t stand for it. Not now, not ever, do you understand me?! I\'m the Doctor, the Oncoming Storm - and you basically meant beat them in a football match, didn\'t you? I\'m the Doctor. Well, they call me the Doctor. I don\'t know why. I call me the Doctor too. I still don\'t know why.</p>')

    D = Category(category_name='Whiteboarding', category_description='About preparing for whiteboarding challenges')
    E = Category(category_name='Code challenge', category_description='About preparing for take home or timed coding challenges')
    F = Category(category_name='Making things', category_description='About learning new technologies to make things with code')

    G = PostCategories(post_id=1, cat_id=1)
    H = PostCategories(post_id=3, cat_id=2)
    I = PostCategories(post_id=3, cat_id=3)
    J = PostCategories(post_id=2, cat_id=2)
    K = PostCategories(post_id=2, cat_id=3)

    db.session.add_all([A, B, C, D, E, F, G, H, I, J, K])
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

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    migrate = Migrate(app, db)
    print 'Connected to DB.'
