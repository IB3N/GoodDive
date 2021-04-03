from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from comments import comments

from functions import sites_all, top_sites, rank_sites, sites_grab_name, comments_grab, user_grab, comment_error_check, comment_insert, average_rating_grab, rating_update, comments_recent

### TODO Remember to import functions from functions.py

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set secret key
app.config.from_mapping(SECRET_KEY='dev')

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

# Configure CS50 Library to use SQLite database
db = SQL('sqlite:///goodive.db')

# Register blueprints for sites
app.register_blueprint(comments)


@app.route('/')
def index():
    """Show user homepage"""
    return render_template('/app/index.html', dropdown=sites_all(), top_sites=top_sites(), recent_comments=comments_recent())


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allow user to register"""
    # User reached page via POST method
    if request.method == 'POST':

        # Retrieve variables from form
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        error = None

        # Check user has entered correct information
        if not username:
            error = 'Username required'
            code = 400
        elif not password:
            error = 'Password required'
            code = 400
        elif not password_check:
            error = 'Password confirmation required'
            code = 400
        elif password != password_check:
            error = 'Passwords do not match'
            code = 400
        elif len(db.execute('SELECT id FROM users WHERE username = :u', u=username)) is not 0:
            error = 'Username taken'
            code = 400

        # If no errors found, insert user into database and log them in
        if error is None:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                        username, generate_password_hash(password))
            user_id = db.execute('SELECT id FROM users WHERE username = :u', u=username)
            session['user_id'] = user_id[0]['id']

            # Send user to index page
            return render_template('/app/index.html', dropdown=sites_all(), top_sites=top_sites())

        # Route user to apology page with respective error and code
        return render_template('/app/apology.html', error=error, code=code, dropdown=sites_all(), top_sites=top_sites())

    # Else user reached page via GET method
    return render_template('/auth/register.html', dropdown=sites_all(), top_sites=top_sites())


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    # If user has reached route via POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = db.execute('SELECT * FROM users WHERE username = :u',
                            u=username)

        if not user:
            error = 'Incorrect username.'
            code = 400
        elif not check_password_hash(user[0]['password'], password):
            error = 'Incorrect password.'
            code = 400

        if error is None:
            session.clear()
            session['user_id'] = user[0]['id']
            return redirect(url_for('index'))

        # Route user to apology page with respective error and code
        return render_template('/app/apology.html', error=error, code=code, dropdown=sites_all(), top_sites=top_sites())

    # Else user has reached route through GET method
    return render_template('/auth/login.html', dropdown=sites_all(), top_sites=top_sites())


@app.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/una-una')
def una_una():
    """ Show user the about Una Una page"""
    return render_template('/nav/unauna.html', dropdown=sites_all(), top_sites=top_sites())


@app.route('/sites')
def sites():
    """Show user the dive sites"""
    return render_template('/nav/sites.html', dropdown=sites_all(), top_sites=top_sites())


@app.route('/about')
def about():
    """Show user about page"""
    return render_template('/nav/about.html', dropdown=sites_all(), top_sites=top_sites())


@app.route('/divesite/<sitename>', methods=('GET', 'POST'))
def divesite(sitename):
    """ Display respective site page using name as input """
    # Grab site information
    site_info = sites_grab_name(sitename)

    # Check for logged in user
    if session.get('user_id') is None:
        return render_template(f'/sites/{sitename}.html', site_name_lower=sitename, site_name=site_info[0]['display_name'], rating=site_info[0]['rating'], username=None, comments=comments_grab(site_info[0]['id']), dropdown=sites_all(), top_sites=top_sites())

    # Retrieve user details
    user = user_grab(session['user_id'])

    # POST method
    if request.method == 'POST':

        # Grab form inputs
        title = request.form.get('title')
        comment = request.form.get('comment')
        rating = request.form.get('rating')

        # Check for valid input
        valid_input = comment_error_check(title, comment, rating)
        error = valid_input['error']

        # Insert review into DB and reload page with updated info
        if error is None:

            # Insert comment into DB
            comment_insert(session['user_id'], site_info[0]['id'], title, comment, rating)

            # Query and grab new average site rating
            rating_new = average_rating_grab(site_info[0]['id'])
            # Update rating in DB
            rating_update(rating_new, sitename)

            # Return user to site page
            return render_template(f'/sites/{sitename}.html', site_name_lower=sitename, site_name=site_info[0]['display_name'], rating=rating_new, username=user[0]['username'], comments=comments_grab(site_info[0]['id']), dropdown=sites_all(), top_sites=top_sites())

        # Errors
        return render_template('/app/apology.html', error=error, code=valid_input['code'], dropdown=sites_all(), top_sites=top_sites())

    # GET method
    return render_template(f'/sites/{sitename}.html', site_name_lower=sitename, site_name=site_info[0]['display_name'], rating=site_info[0]['rating'], username=user[0]['username'], comments=comments_grab(site_info[0]['id']), dropdown=sites_all(), top_sites=top_sites())


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template('/app/apology.html', error=e.name, code=e.code, dropdown=sites_all(), top_sites=top_sites())


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)