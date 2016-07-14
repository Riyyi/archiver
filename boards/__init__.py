from flask import Flask, render_template, url_for, flash

# My classes
from models.base_model import db
from models.data_model import Category, Board, Thread, Thread_Post, Post, Image, Image_Tag, Tag, Rank, User, Que
from models.que_form import QueForm
from db_connect import connection
from que import add_to_que
from timefunc import convert_utc_datetime
from string_converter import convert_str_to_int

# 4chan scraping API
from basc_py4chan import Board as chanBoard
from basc_py4chan import Thread as chanThread

# Garbage collection
import gc
# Human readable data
import humanize
# Unescape html comments

import time
import datetime
from datetime import timezone
from dateutil import tz

#pprint(var)
from pprint import pprint

app = Flask(__name__)
db_host, db_username, db_password, db_database = connection()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'C*<$UH<#H*(UH9mu<(#*)M)#(MIoPhD+'
db.init_app(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/index')
@app.route('/')
def index():
    category = Category.query.all()

    gc.collect()
    return render_template('index.html', categories = category)

@app.route('/<board>/')
@app.route('/<board>/<int:page>')
def board(board, page=1):
    # Get the Board
    get_board = Board.query.filter_by(url = board).first()

    # If board doesn't exist, render 404 page
    if get_board == None:
        return render_template('404.html')

    # Get all the Threads data
    get_threads = Thread.query.filter_by(board_ID = get_board.ID)
    # Count the number of pages
    pages = int(get_threads.count() / 15) + 1
    # Get only the Threads from the current page
    get_threads = get_threads[page * 15 - 15:page * 15]

    # Get the first 4 posts of each Thread
    get_posts = []
    for thread in get_threads:
        # Get all the Posts of the Thread
        tmp_thread = Post.query.join(Thread_Post).filter(Thread_Post.thread_ID == thread.ID)
        # Get the OP op the Thread
        tmp_op = tmp_thread[:1]
        # Get the 3/5 latest Thread Posts
        tmp_post = tmp_thread[-get_board.posts_shown:]

        # Remove the first element (OP) from the Posts if the total is less than the board specified
        if tmp_thread.count() <= 5:
            tmp_post.pop(0)

        # Add the OP + latest posts in a list of a list
        get_posts.append(tmp_op + tmp_post)

    #test = datetime.datetime(1344570123, tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/Amsterdam'))
    #print(test)

    #test2 = datetime.datetime.fromtimestamp(1344570123).strftime('%m/%d/%Y(%a)%H:%M:%S')
        #test2 = datetime.datetime.fromtimestamp(1344570123, tz=tz.tzlocal()).strftime('%m/%d/%Y(%a)%H:%M:%S')
        #print(test2)
    #12/28/15(Mon)16:31:49

    #test2 = test2.replace(tzinfo=tz.tzlocal())
    #print(test2)

    #1344570123
    # timezone.UTC
    # tz.tzlocal()


    gc.collect()
    return render_template('board.html', board = get_board, thread = get_threads, threads = get_posts, pages=pages, page = page,
                           humanize = humanize, convert_utc_datetime = convert_utc_datetime, strtoint = convert_str_to_int)

@app.route('/<board>/thread/<int:thread_id>')
def thread(board, thread_id):
    # Get the Board
    get_board = Board.query.filter_by(url = board).first()
    # If Board doesn't exist, render 404 page
    if get_board == None:
        return render_template('404.html')

    # Find the Thread in the Thread_Post table
    get_thread = Thread_Post.query.join(Post).join(Thread).join(Board).filter(
        Board.url == get_board.url, Thread_Post.thread_ID == Thread.ID, Thread_Post.post_ID == Post.ID, Post.no == thread_id).first()
    # If Thread doesn't exist, render 404 page
    if get_thread == None:
        return render_template('404.html')

    # Get all of the Posts in this Thread
    thread = Post.query.join(Thread_Post).filter(Thread_Post.thread_ID == get_thread.thread_ID).all()

    return render_template('thread.html', board = get_board, thread = thread)

@app.route('/about')
def about():
    title = 'About this site'
    paragraph = ['paragraph', 'blablablabla']

    return render_template('about.html', title = title, paragraph = paragraph)

@app.route('/que', methods=['GET', 'POST'])
def que():
    # Form Object
    que_form = QueForm()
    if que_form.validate_on_submit():
        pprint('SUBMITTED AND VALIDATED!')

        # URL input
        url = que_form.url.data

        # Add the Thread to the Que (returns errors)
        errors = add_to_que(url)

        # Add the errors to the form
        for error in errors:
            que_form.url.errors.append(error)

        pprint(errors)

    #que = db.session.query(Que).all()
    que = Que.query.all()

    gc.collect()
    return render_template('que.html', form = que_form, ques = que)

@app.route('/database')
def database():
    try:

        #guest = User('guest', 'guestpassword', 'guest@example.com', 'salt')
        #db.session.add(guest)
        #db.session.commit()

        users = User.query.all()
        admin = User.query.filter_by(username='admin').first()

        # for instance in User.query.order_by(User.ID):
        #     print(instance.username, instance.password, instance.email)

        # for username, password in db.session.query(User.username, User.password):
        #     print(username, password)

        # for row in db.session.query(User, User.username).all():
        #     print(row.User, row.username)

        #for instance in Category.query:
        #    print(instance.name)

        for instance in Board.query:
             print(instance.title, instance.url, instance.category_ID, instance.category.name)

        for i in db.session.query(Board).join(Category).filter(Category.ID == 1).all():
           print(i.title, i.category.name)

        for instance in Board.query.join(Category).filter(Category.ID == 1):
            print(instance.title, instance.category.name)

        for i in Category.query.first().boards:
            print(i.title)

        for instance in Thread.query:
            print(instance.ID, instance.board_ID, instance.board.title)

        gc.collect()

        #pprint.pprint(users)
        return(str(users))
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.debug = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug = app.debug)

# // Calculate new image size
# 250, 250 < SIZE
# if ($image_width > MAX_W || $image_height > MAX_H) {
#     $scale_w = MAX_W / $image_width;
#     $scale_h = MAX_H / $image_height;
#     ($scale_w < $scale_h) ? $scale = $scale_w : $scale = $scale_h;
#     $new_width = ceil($image_width * $scale) + 1;
#     $new_height = ceil($image_height * $scale) + 1;
# } else {
#     $new_width = $image_width;
#     $new_height = $image_height;
# }

#width,height=im.size
#import Image; im = Image('whatever.png')

#https://stackoverflow.com/questions/2612436/create-thumbnail-images-for-jpegs-with-python
#https://stackoverflow.com/questions/8631076/what-is-the-fastest-way-to-generate-image-thumbnails-in-python