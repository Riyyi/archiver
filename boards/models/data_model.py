from models.base_model import db, Base, Integer
from sqlalchemy.dialects.mysql import TINYINT

class Category(db.Model, Base):
    name = db.Column(db.String(45), unique=True, nullable=False)
    nsfw = db.Column(TINYINT(unsigned=True))

    boards = db.relationship('Board', back_populates='category')

    def __repr__(self):
        return "<Category(name='%s', nsfw='%s')>" % (
            self.name, self.nsfw)

class Board(db.Model, Base):
    title = db.Column(db.String(45), unique=True)
    keywords = db.Column(db.String(255))
    description = db.Column(db.String(255))
    url = db.Column(db.String(12), unique=True, nullable=False)

    category_ID = db.Column(Integer(unsigned=True), db.ForeignKey('category.ID'), nullable=False)
    category = db.relationship('Category', back_populates='boards')

    threads = db.relationship('Thread', back_populates='board')

    posts_shown = db.Column(TINYINT(unsigned=True), nullable=False)
    posting_enabled = db.Column(db.Integer)

    def __repr__(self):
        return "<Board(title='%s', keywords='%s', description='%s', url='%s', 'posting_enabled='%s')>" % (
            self.title, self.keywords, self.description, self.url, self.posting_enabled)

class Thread(db.Model, Base):
    board_ID = db.Column(Integer(unsigned=True), db.ForeignKey('board.ID'), nullable=False)
    board = db.relationship('Board', back_populates='threads')

    sticky = db.Column(TINYINT(unsigned=True), nullable=False)
    closed = db.Column(TINYINT(unsigned=True), nullable=False)
    archived = db.Column(TINYINT(unsigned=True), nullable=False)

    thread_posts = db.relationship('Thread_Post', back_populates='thread')

    def __repr__(self):
        return "<Thread(ID='%s', board='%s' sticky='%s', closed='%s', archived='%s')>" % (
            self.ID, self.board_ID, self.sticky, self.closed, self.archived)

class Thread_Post(db.Model, Base):
    thread_ID = db.Column(Integer(unsigned=True), db.ForeignKey('thread.ID'), nullable=False)
    thread = db.relationship('Thread', back_populates='thread_posts')

    post_ID = db.Column(Integer(unsigned=True), db.ForeignKey('post.ID'), nullable=False)
    post = db.relationship('Post', back_populates='thread_posts')

    ques = db.relationship('Que', back_populates='thread_post')

    def __repr__(self):
        return "<Thread_Post(ID='%s', thread='%s' post='%s')>" % (
            self.ID, self.thread_ID, self.post_ID)

class Post(db.Model, Base):
    no = db.Column(db.Integer, nullable=False)
    poster_id = db.Column(db.Text, nullable=True)

    rank_ID = db.Column(Integer(unsigned=True), db.ForeignKey('rank.ID'))
    rank = db.relationship('Rank', back_populates='posts')

    name = db.Column(db.Text, nullable=False)
    tripcode = db.Column(db.Text)
    subject = db.Column(db.Text)
    html_comment = db.Column(db.Text)
    text_comment = db.Column(db.Text)
    timestamp = db.Column(Integer(unsigned=True), nullable=False)

    image_ID = db.Column(Integer(unsigned=True), db.ForeignKey('image.ID'))
    image = db.relationship('Image', back_populates='posts')

    file_deleted = db.Column(TINYINT(unsigned=True))
    spoiler = db.Column(TINYINT(unsigned=True))

    thread_posts = db.relationship('Thread_Post', back_populates='post')

    def __repr__(self):
        return "<Post(ID='%s', no='%s')>" % (self.ID, self.no)

class Que(db.Model, Base):
    thread_post_ID = db.Column(Integer(unsigned=True), db.ForeignKey('thread_post.ID'), nullable=False)
    thread_post = db.relationship('Thread_Post', back_populates='ques')

    def __repr__(self):
        return "<Que(ID='%s', thread_post='%s')>" % (self.ID, self.thread_post_ID)

class Image(db.Model, Base):
    name = db.Column(nullable=False)
    name_original = db.Column(nullable=False)
    extension = db.Column(nullable=False)
    size = db.Column(nullable=False)
    md5 = db.Column(nullable=False)
    width = db.Column(nullable=False)
    height = db.Column(nullable=False)
    thumbnail_width = db.Column(nullable=False)
    thumbnail_height = db.Column(nullable=False)

    posts = db.relationship('Post', back_populates='image')
    image_tags = db.relationship('Image_Tag', back_populates='image')

class Image_Tag(db.Model, Base):
    image_ID = db.Column(Integer(unsigned=True), db.ForeignKey('image.ID'), nullable=False)
    image = db.relationship('Image', back_populates='image_tags')

    tag_ID = db.Column(Integer(unsigned=True), db.ForeignKey('tag.ID'), nullable=False)
    tag = db.relationship('Tag', back_populates='image_tags')

class Tag(db.Model, Base):
    name = db.Column(db.String(255), nullable=False)

    image_tags = db.relationship('Image_Tag', back_populates='tag')

class Rank(db.Model, Base):
    capcode = db.Column(db.Text(12), nullable=False)
    display_name = db.Column(db.Text(12), nullable=True)
    rank = db.Column(db.Integer, nullable=False, default=1000)
    colour = db.Column(db.String(45))
    image = db.Column(db.String(45))

    posts = db.relationship('Post', back_populates='rank')
    users = db.relationship('User', back_populates='rank')

class User(db.Model, Base):
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64))
    salt = db.Column(db.String(64), nullable=False)

    rank_ID = db.Column(Integer(unsigned=True), db.ForeignKey('rank.ID'))
    rank = db.relationship('Rank', back_populates='users')

    def __init__(self, username, password, email, salt):
        self.username = username
        self.password = password
        self.email = email
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % self.username