import functools

from cs50 import SQL
from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from statistics import mean

from functions import username_grab, sites_grab, comments_grab, comment_insert, update_rating

dive_sites = Blueprint('dive_sites', __name__, url_prefix='/divesites')

# Configure CS50 library to use SQLite database
db = SQL('sqlite:///goodive.db')

@dive_sites.route('/apollo', methods=('GET', 'POST'))
def apollo():
    """Show user Apollo"""
    # Create site function unique variables to send to 'sitelayout.html'
    site_name = 'Apollo'
    site_name_lower = 'apollo'

    # Grab site and user information
    site_info = sites_grab(site_name_lower)
    if session['user_id']:
        username = username_grab(session['user_id'])

    # User has reached route via POST
    if request.method == 'POST':

        # Grab form inputs from apollo comment
        title = request.form.get('title')
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        error = None

        # Check for valid input
        if not title:
            error = 'Title is required'
            code = 400
        elif not comment:
            error = 'Please leave a comment'
            code = 400
        elif not rating:
            error = 'Please rate this divesite'
            code = 400

        # If no error, insert users comment into database and reload page with comment and updated info
        if error is None:

            # Insert comment into database
            comment_insert(session['user_id'], site_info[0]['id'], title, comment, rating)

            # Update site rating
            rating_new = mean([site_info[0]['rating'], rating])
            update_rating(rating_new, site_name_lower)

            # Grab updated site comments
            comments = comments_grab(site_info[0]['id'])


            return render_template('/sites/apollo.html', site_name=site_name, site_name_lower=site_name_lower, rating=comments=comments)

        return render_template('/app/apology.html', error=error, code=code)

    # Else user has reached route via GET
    comments = comments_grab(site_info[0]['id'])
    return render_template('/sites/apollo.html', site_name=site_name, site_name_lower=site_name_lower, rating=site_info[0]['rating'], username=username, comments=comments)


@dive_sites.route('/artemis', methods=('GET', 'POST'))
def artemis():
    """Show user Artemis"""
    site_name = 'Artemis'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/artemis.html')

    # Else user has reached route via GET
    return render_template('/sites/artemis.html', site_name=site_name)


@dive_sites.route('/barrenland', methods=('GET', 'POST'))
def barren_land():
    """Show user Barrenland"""
    site_name = 'Barrenland'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/barrenland.html')

    # Else user has reached route via GET
    return render_template('/sites/barrenland.html', site_name=site_name)


@dive_sites.route('/batugila', methods=('GET', 'POST'))
def batu_gila():
    """Show user Batu Gila"""
    site_name = 'Batu Gila'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/batugila.html', site_name=site_name)

    # Else user has reached route via GET
    return render_template('/sites/batugila.html')


@dive_sites.route('/blackforest', methods=('GET', 'POST'))
def black_forest():
    """Show user Black Forest"""
    site_name = 'Black Forest'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/blackforest.html')

    # Else user has reached route via GET
    return render_template('/sites/blackforest.html', site_name=site_name)


@dive_sites.route('/hongkong', methods=('GET', 'POST'))
def hong_kong():
    """Show user Hong Kong"""
    site_name = 'Hong Kong'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/hongkong.html')

    # Else user has reached route via GET
    return render_template('/sites/hongkong.html', site_name=site_name)


@dive_sites.route('/housereef', methods=('GET', 'POST'))
def house_reef():
    """Show user House Reef"""
    site_name = 'House Reef'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/housereef.html')

    # Else user has reached route via GET
    return render_template('/sites/housereef.html', site_name=site_name)


@dive_sites.route('/ihana', methods=('GET', 'POST'))
def ihana():
    """Show user Ihana"""
    site_name = 'Ihana'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/ihana.html')

    # Else user has reached route via GET
    return render_template('/sites/ihana.html', site_name=site_name)


@dive_sites.route('/jackpoint', methods=('GET', 'POST'))
def jack_point():
    """Show user Jack Point"""
    site_name = 'Jack Point'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/jackpoint.html')

    # Else user has reached route via GET
    return render_template('/sites/jackpoint.html', site_name=site_name)


@dive_sites.route('/jungle', methods=('GET', 'POST'))
def jungle():
    """Show user Jungle"""
    site_name = 'Jungle'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/jungle.html')

    # Else user has reached route via GET
    return render_template('/sites/jungle.html', site_name=site_name)


@dive_sites.route('/kingston', methods=('GET', 'POST'))
def kingston():
    """Show user Kingston Wall"""
    site_name = 'Kingston Wall'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/kingston.html')

    # Else user has reached route via GET
    return render_template('/sites/kingston.html', site_name=site_name)


@dive_sites.route('/pinnacle1', methods=('GET', 'POST'))
def pinnacle1():
    """Show user Pinnacle 1"""
    site_name = 'Pinnacle 1'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/pinnacle1.html')

    # Else user has reached route via GET
    return render_template('/sites/pinnacle1.html', site_name=site_name)


@dive_sites.route('/pinnacle2', methods=('GET', 'POST'))
def pinnacle2():
    """Show user Pinnacle 2"""
    site_name = 'Pinnacle 2'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/pinnacle2.html')

    # Else user has reached route via GET
    return render_template('/sites/pinnacle2.html', site_name=site_name)


@dive_sites.route('/satellite', methods=('GET', 'POST'))
def satellite():
    """Show user Satellite"""
    site_name = 'Satellite'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/satellite.html')

    # Else user has reached route via GET
    return render_template('/sites/satellite.html', site_name=site_name)


@dive_sites.route('/valtimo', methods=('GET', 'POST'))
def valtimo():
    """Show user Valtimo"""
    site_name = 'Valtimo'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/valtimo.html')

    # Else user has reached route via GET
    return render_template('/sites/valtimo.html', site_name=site_name)


@dive_sites.route('/wreckjam', methods=('GET', 'POST'))
def wreck_jam():
    """Show user Wreck & Jam"""
    site_name = 'Wreck & Jam'
    # User has reached route via POST
    if request.method == 'POST':
        return render_template('/sites/wreckjam.html')

    # Else user has reached route via GET
    return render_template('/sites/wreckjam.html', site_name=site_name)