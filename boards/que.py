#!/usr/bin/python

# My classes
from models.base_model import db, Base
from models.data_model import Category, Board, Thread, Thread_Post, Post, Image, Image_Tag, Tag, Rank, User, Que
from db_connect import connection

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# CLI interface helper
import click
# Regex
from re import search

# 4chan scraping API
from basc_py4chan import Board as chanBoard
from basc_py4chan import Thread as chanThread
from basc_py4chan import Post as chanPost
from basc_py4chan import File as chanFile

# Python sleep
import time

# Image downloading
import urllib.request

# Garbage collection
import gc

#pprint(var)
from pprint import pprint

# TMP!
import html


db_host, db_username, db_password, db_database = connection()
engine = create_engine('mysql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_database)

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@click.command()
@click.option('-A', '--add', help = '4chan URL to add to the Que.')
def executable(add):
    if not add:
        main()
    else:
        errors = add_to_que(add)
        for error in errors:
            print(error)

def main():
    # Main Que archive loop
    pprint('Main')

    # loop through all ques
    #   get_board
    #   get_thread
    #
    #   loop through thread
    #      loop through all posts of this thread
    #      add post if not already added

    while True:
        ques = session.query(Que).all()

        # Loop through all Ques
        for que in ques:
            board_id = que.thread_post.thread.board.url
            thread_id = que.thread_post.thread_ID

            # Get the Thread
            alive, board, thread = get_thread(board_id, que.thread_post.post.no)

            if not alive:
                # Mark Thread closed
                thread_db = session.query(Thread).filter_by(ID = thread_id).first()
                thread_db.closed = 1

                # Check if Thread is archived
                if thread:
                    if thread.archived:
                        thread_db.archived = 1

                # Remove from Ques
                session.delete(que)
                session.commit()
            else:
                # Get all Posts of this Thread from the DB
                posts = session.query(Post).join(Thread_Post).filter(Thread_Post.thread_ID == thread_id).all()

                # Loop through Thread
                for chanPost in thread.all_posts:
                    added = False
                    # Loop through Thread on the DB
                    for post in posts:
                        if chanPost.post_id == post.no:
                            added = True

                    if not added:
                        # Check if Rank currently already exists
                        rank = add_rank(chanPost.poster_capcode)

                        # Save the Image (and thumbnail)
                        image = add_img(chanPost.file)

                        add_post(chanPost, rank, image, que.thread_post.thread_ID)
                    else:
                        # Check if the image was deleted, and update the Post accordingly
                        if chanPost.has_file:
                            if chanPost.file.file_deleted == 1 and post.file_deleted == 0:
                                post.file_deleted = 1
                                session.commit()
            time.sleep(1)

        gc.collect()
        time.sleep(10 - len(ques))
        #print('Que length: ' + str(len(ques)))
        #print('ALL QUES ROTATED')

def add_post(postObj, rank_ID, image_ID, thread_ID):
    # Add Post to the DataBase

    # Stop the script if 'postObj' is not a valid 'BASC-py4chan.Post' object
    if not isinstance(postObj, chanPost):
        return None

    # Check if the Post actually has a file
    if postObj.has_file:
        file_deleted = postObj.file.file_deleted
        spoiler = postObj.file.file_spoiler
    else:
        file_deleted = None
        spoiler = None

    # Safely escape html in subject
    if postObj.subject:
        subject = html.unescape(postObj.subject)
    else:
        subject = None

    # Add the Post
    post_db = Post(no = postObj.post_id, poster_id = postObj.poster_id, rank_ID = rank_ID, name = html.unescape(postObj.name),
                   tripcode = postObj.tripcode, subject = subject,
                   html_comment = postObj.html_comment, text_comment = postObj.text_comment,
                   timestamp = postObj.timestamp, image_ID = image_ID, file_deleted = file_deleted,
                   spoiler = spoiler)
    session.add(post_db)
    session.commit()

    # Add the Thread_Post link-table
    thread_post_db = Thread_Post(thread_ID = thread_ID, post_ID = post_db.ID)
    session.add(thread_post_db)
    session.commit()

    return thread_post_db

def add_to_que(url):
    # Add Que to the DataBase
    pprint('Add')

    errors = []

    # Check if it is a valid 4chan Thread URL
    pattern = 'https?:\/\/boards.4chan.org\/[a-z]+\/thread\/[0-9]+\/?'
    url_valid = search(pattern, url)

    # @Todo: length between 34,60

    if not url_valid:
        errors.append('Invalid 4chan URL.')
    else:
        # Get board
        # Taken the 's' in https:// into account, cut the first part before the board of the URL off
        # [http(s)://boards.4chan.org/] b/thread/688737072/#p688761325
        if url.find('s') == 4:
            board_id = url[25:]
        else:
            board_id = url[24:]
        # Cut the last part after the board of the URL off
        # b [/thread/688737072/]
        board_id = board_id[:board_id.find('/')]

        # Get thread
        # Cut off first part before the thread number of the URL off
        # [https://boards.4chan.org/b/thread/] 688737072/#p688761325
        thread_id = url[url.find('/thread/') + 8:]
        # Chop off '/' and '#' at the end
        # 688737072 [/] [#p68876132]
        if thread_id.find('/') != -1:
            thread_id = thread_id[:thread_id.find('/')]
        if thread_id.find('#') != -1:
            thread_id = thread_id[:thread_id.find('#')]

        # Get the chanThread
        alive, board, thread = get_thread(board_id, thread_id)

        #alive = False
        #################################
        pprint(thread.topic.poster_capcode)
        #################################

        if not alive:
            errors.append('This thread has been pruned or deleted.')
        else:
            # Checkif thread is not already Que'd
            # @Todo: change to .join statements, like in Board!!!!!!!!!!!!!!!!
            thread_exists = session.query(Post).filter_by(no = thread_id).first()
            if thread_exists:
                que_exists = session.query(Thread_Post).filter_by(post_ID = thread_exists.ID).first()
                que_exists = session.query(Que).filter_by(thread_post_ID = que_exists.ID).first()
            else:
                que_exists = None
            board_exists = session.query(Board).filter_by(url = board_id).first()

            if not board_exists:
                errors.append('This board does not exist (yet), ask Rick about it.')
            else:
                # Add the Thread
                if not thread_exists:
                    thread_db = Thread(board_ID = board_exists.ID, sticky = thread.sticky, closed = thread.closed,
                                       archived = thread.archived)
                    session.add(thread_db)
                    session.commit()

                    # chanPost object
                    topic = thread.topic

                    # Check if Rank currently already exists
                    rank = add_rank(topic.poster_capcode)

                    # Save the Image (and thumbnail)
                    image = add_img(topic.file)

                    thread_post_db = add_post(topic, rank, image, thread_db.ID)
                else:
                    thread_post_db = session.query(Thread_Post).filter_by(post_ID = thread_exists.ID).first()

                # Add the Thread to the Que
                if not que_exists:
                    session.add(Que(thread_post_ID = thread_post_db.ID))
                    session.commit()

    gc.collect()
    return errors

def add_rank(rank):
    # Add Rank to the DataBase

    rank_id = None
    # Check for a possible rank
    if not rank == None:
        rank_exists = session.query(Rank).filter_by(capcode = rank).first()
        if rank_exists:
            rank_id = rank_exists.ID
        else:
            rank_db = Rank(capcode = rank, rank=1000)
            session.add(rank_db)
            session.commit()
            rank_id = rank_db.ID

    return rank_id

def save_img(url, path, name):
    # Save the image to disc

    response = urllib.request.urlopen(url)
    data = response.read()

    # Chop off the first trailing slash '/' of the path
    if path.find('/') == 0:
        path = path[1:]

    with open(path + name, 'wb') as f:
        f.write(data)

def add_img(fileObj):
    # Add Image to the DataBase

    # Stop the script if 'fileObj' is not a valid 'BASC-py4chan.File' object
    if not isinstance(fileObj, chanFile):
        return None

    image_id = None
    # Check if Image already exists
    file_exists = session.query(Image).filter_by(md5 = fileObj.file_md5_hex).first()
    if not file_exists:
        # Remove .jpg/.png at the end of the file name
        filename = fileObj.filename
        if filename.find('.') != -1:
            filename = filename[:filename.find('.')]

        # Remove .jpg/.png at the end of the original file name
        filename_original = fileObj.filename_original
        if filename.find('.') != -1:
            filename_original = filename_original[:filename_original.find('.')]

        # Save the Image and the thumbnail
        save_img(fileObj.file_url,      'static/img/', filename + fileObj.file_extension)
        save_img(fileObj.thumbnail_url, 'static/img/', filename + 's.jpg')

        # Add to the DataBase
        image_db = Image(name = filename, name_original = filename_original, extension = fileObj.file_extension,
                         size = fileObj.file_size, md5 = fileObj.file_md5_hex,
                         width = fileObj.file_width, height = fileObj.file_height,
                         thumbnail_width = fileObj.thumbnail_width, thumbnail_height = fileObj.thumbnail_height)
        session.add(image_db)
        session.commit()

        image_id = image_db.ID

    return image_id

def get_thread(board_id, thread_id):
    # Get the Thread and return if 'closed' or not

    alive = False
    board = chanBoard(board_id)
    thread = None
    if board.thread_exists(thread_id):
        thread = board.get_thread(thread_id)
        if not thread.closed:
            alive = True
        else:
            print('Thread is not alive')

    return alive, board, thread

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# db_host, db_username, db_password, db_database = connection()
# engine = create_engine('mysql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_database)
#
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind = engine)
# session = DBSession()
#
#
# category = session.query(Category).all()
# pprint(category)
#
# gc.collect()


if __name__ == '__main__':
    executable()
