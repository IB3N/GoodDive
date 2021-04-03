from flask import redirect, render_template, request, session
from functools import wraps

from cs50 import SQL

# Load database
db = SQL('sqlite:///goodive.db')

""" APPLICATION FUNCTIONS """

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


""" USERS TABLE QUERY'S """

def user_grab(session_id):
    """ Queries SQL database for username """

    user = db.execute('SELECT username FROM users WHERE id = :i',
                        i=session_id)
    return user


""" SITES TABLE QUERY """

def sites_all():
    """ Query for all sites """

    sites = db.execute('SELECT * FROM sites ORDER BY name')
    return sites


def sites_grab_name(site):
    """ Queries SQL database for site_id """

    site = db.execute('SELECT * FROM sites WHERE name = :n',
                n=site)
    return site


def sites_grab_id(id):
    """ Query for site name using comment id """

    # Get site name and return user to that site page
    site = db.execute('SELECT name, sites.id FROM sites JOIN comments ON sites.id = comments.site_id WHERE sites.id = (SELECT site_id FROM comments WHERE id = :i) LIMIT 1',
                            i=id)
    return site


def average_rating_grab(site_id):
    """ Query for average site rating"""

    avg = db.execute('SELECT avg(rating) FROM comments WHERE site_id = :s',
                        s=site_id)
    return avg[0]['avg(rating)']


def rating_update(rating, sitename):
    """ Updates rating with new rating average """

    db.execute('UPDATE sites SET rating = :r WHERE name = :n',
                r=rating, n=sitename)


def rank_sites():
    """ Get top 5 rated dive sites """

    sites = db.execute('SELECT * FROM sites ORDER BY rating DESC')
    return sites


def top_sites():
    """ Get top 5 rated dive sites """

    top = db.execute('SELECT * FROM sites ORDER BY rating DESC LIMIT 10')
    return top


""" COMMENTS TABLE QUERY'S """

def comments_grab(site_id):
    """ Queries SQL database for comment list from using site id """

    site_comments = db.execute('SELECT username, comments.id, user_id, title, comment, rating, created FROM comments JOIN users ON users.id = comments.user_id WHERE site_id = :s ORDER BY created DESC',
                                s=site_id)
    return site_comments


def comment_grab(id):
    """ Grab one single comment using comment id """

    # Select comment from db using comment id
    comment = db.execute('SELECT * FROM comments WHERE id = :c',
                        c=id)
    return comment


def comment_insert(session_id, site_id, title, comment, rating):
    """ Inserts comment data into SQL database """

    db.execute('INSERT INTO comments (user_id, site_id, title, comment, rating) VALUES (?, ?, ?, ?, ?)',
                session_id, site_id, title, comment, rating)


def comment_update(title, comment, rating, id):
    """ Update comment from edit comment page """

    update = db.execute('UPDATE comments SET title = :t, comment = :c, rating = :r WHERE id = :i',
                        t=title, c=comment, r=rating, i=id)
    return update

def comment_delete(id):
    """ Delete single comment by given id """

    # Delete comment from e
    delete = db.execute('DELETE FROM comments WHERE id = :i',
            i=id)
    return delete


def comment_error_check(title, comment, rating):
    """ Checks form for valid input """

    error = None
    code = None

    if not title:
        error = 'Title is required'
        code = 400
    elif not comment:
        error = 'Please leave a comment'
        code = 400
    elif not rating:
        error = 'Please rate this divesite'
        code = 400

    return {
        'error': error,
        'code': code
    }


def comments_error_check(comment):
    """ Check for edit errors """

    error = None
    code = None

    # Check post validity
    if not comment:
        error = 'Post not found'
        code = 404

    # Check author validity
    elif session['user_id'] != int(comment[0]['user_id']):
        error = 'You don\'t have permission to access this post'
        code = 403

    return {
        'error': error,
        'code': code
    }


def comments_recent():
    """ Query for most recent comments """

    recent = db.execute('SELECT * FROM comments JOIN sites ON comments.site_id = sites.id JOIN users ON comments.user_id = users.id ORDER BY created DESC LIMIT 10')
    return recent