import functools

from cs50 import SQL
from flask import Blueprint, flash, session, redirect, render_template, request, url_for

from functions import sites_all, top_sites, login_required, comment_grab, comment_delete, sites_grab_id, comment_update, average_rating_grab, rating_update, comments_error_check

comments = Blueprint('comments', __name__, url_prefix='/comments')


@comments.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """ Allow user to edit comment """
    # Query for comment
    old_comment = comment_grab(id)
    check = comments_error_check(old_comment)

    # Check for comment grab error
    if check['error'] is None:

        # POST route
        if request.method == 'POST':

            # Retrieve form input from edit.html
            title = request.form.get('title')
            comment = request.form.get('comment')
            rating = request.form.get('rating')

            update = comment_update(title, comment, rating, id)

            # If error
            if update != 1:
                return render_template('/app/apology.html', error='Couldn\'t update comment', code=500, dropdown=sites_all(), top_sites=top_sites())

            # Query for site name and return user to respective page
            site = sites_grab_id(id)
            site_name_lower = site[0]['name']

            # No errors, check for rating edit
            if rating == old_comment[0]['rating']:
                return redirect(url_for('divesite', sitename=site_name_lower))

            # Rating has been edited
            # Retrieve new average rating
            rating_new = average_rating_grab(site[0]['id'])
            rating_update(rating_new, site_name_lower)

            return redirect (url_for('divesite', sitename=site_name_lower))

        # GET route
        return render_template('/comments/edit.html', comment=old_comment)

    # Route user to apology page due to error
    return render_template('/app/apology.html', error=old_comment['error'], code=old_comment['code'], dropdown=sites_all(), top_sites=top_sites())

@comments.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """ Allow users to delete their comment """
    # Query for comment and site name
    comment = comment_grab(id)
    check = comments_error_check(comment)
    site = sites_grab_id(id)
    site_name_lower = site[0]['name']

    # Check for comment grab error
    if check['error'] is None:

        comment_delete(id)

        # Check for delete comment function error
        if delete is False:

            return render_template('/app/apology.html', error='Could not delete comment', code=500, dropdown=sites_all(), top_sites=top_sites())

        # No errors, update rating
        rating_new = average_rating_grab(site[0]['id'])
        rating_update(rating_new, site_name_lower)

        # Redirect user back to respective site page
        return redirect(url_for('divesite', sitename=site_name_lower))

    # Route user to apology page due to error
    return render_template('/app/apology.html', error=check['error'], code=check['code'], dropdown=sites_all(), top_sites=top_sites())