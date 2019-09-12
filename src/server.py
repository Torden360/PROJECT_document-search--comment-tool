from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, jsonify, make_response, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Document, Search, Search_Match, Group, Note, connect_to_db, db) 
from db_functions import load_text, store_search, create_user, create_group, store_match, store_notes

from sqlalchemy import func, distinct, update
# I don't know yet if I'll use these

from werkzeug.utils import secure_filename

from search import search
# imports regex function search

import random

import os


app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def display_user_homepage():
    """ Displays user homepage """

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user.is_doc_owner:
    # if the user stored in the session is the doc_owner, then redirect to doc_owner homepage
    # need to also add if user is owner of the document requested
        return redirect('/owner_home')

    else:
    # if the user is simply a contributor, redirect to user_homepage
    # need to shift some things around to accomodate for if user also owns a document but not this one
        doc_id = session.get('did')
        file = Document.query.get(doc_id)

        return render_template('user_homepage.html', file=file)


@app.route('/user_groups')
def display_groups():
    """ Displays user's groups on window load """

    doc_id = session.get('did')
    user_id = session.get('user_id')

    file = Document.query.get(doc_id)

    searches = file.searches

    groups = []
    # create groups list

    for user_search in searches:
        group = user_search.groups
        # get the group associated with the current search in the loop

        search_tuples = []
        # create search data list

        if group and group[0].user_id == user_id:
        # if group, if group belongs to current user

            search_phrase = user_search.search_phrase
            search_tuples.append(search_phrase)
            # append search_phrase

            matches = user_search.search_matches
            matches_list = []
            # create matches list

            search_tuples.append(matches_list)
            # append matches list to search data list

            for match in matches:
                match_data = (match.match_content, match.match_id)
                # create a tuple for each match containing the match_content and match_id)

                notes = match.notes
                # creates a list of match notes

                content = []
                # create a content list

                content.append(match_data)
                # add match_data tuple to content list

                if notes:
                    note = (notes[0].note_content, notes[0].note_id)
                    # only be one note per match, but need to index because is a list
                    # create a tuple containing note_content and note_id

                    content.append(note)
                    # add note tuple to content list

                content = tuple(content)
                # make content list a tuple

                matches_list.append(content)
                # add content tuple to list of matches

            # search_tuples.append(matches_list)
            # add list of match content tuples to search data list
            # I believe I did this earlier, and this line is redundant

            search_tuples = tuple(search_tuples)
            # make search data list into a tuple

            groups.append(search_tuples)
            # add search data tuple of tuples of list of tuples into groups list

    if not Group.query.filter_by(user_id=user_id).all():
        flash('You have no saved groups')
        # TODO: this isn't working, check if this is working for new user with no groups

    groups = jsonify(groups)

    return groups


@app.route('/owner_home')
def display_document_owner_homepage():
    """ Displays the document of owner's choice """

    user_id = session.get('user_id')
    user = User.query.get(user_id)
    username = user.username
    # get the user's stored username

    file_objs = Document.query.filter(Document.doc_owner==username).all()
    # get all of the document objects stored under the given username

    files = []
    # create files list

    for file in file_objs:
        files.append((file, bytes.decode(file.text)))
        # add tuple of file object and decoded file text to files list

    return render_template("owner_homepage.html", files=files)


@app.route('/stats_view')
def display_doc_stats():
    """ Displays document statistics for document owner """

    doc_id = request.args.get('did')
    file = Document.query.get(doc_id)

    searches = file.searches
    # get all searches for selected file

    search_phrase_set = set()
    # create a set for search phrases

    search_tuples = []
    # create a set for search data

    for search_obj in searches:
        search_phrase_set.add(search_obj.search_phrase)
        # add the search phrase for each search into the created set to remove duplicates
    
    for search_phrase in search_phrase_set:
        searches_w_phrase = Search.query.filter(Search.search_phrase==search_phrase).all()
        # for each phrase in the set, find all unique searches with that phrase

        count = len(searches_w_phrase)
        # find the length of the generated searches of search phrase list

        search_tuple = (search_phrase, count)
        # create a tuple containing the search phrase and its count 

        search_tuples.append(search_tuple)
        # add the individual search tuples to the search data list

    def Sort_Tuple(tup):
        """ Display search with largest count first """
        return(sorted(tup, key = lambda x: x[1], reverse=True)) 
        # sorts the data in the list of tuples according to second param/search count of each tuple

    search_tuples = Sort_Tuple(search_tuples)
    # call the sort function on the search tuples
    
    return render_template('stats_view.html', file=file, search_tuples=search_tuples)


# --------------------------- UNDER CONSTRUCTION ----------------------------

@app.route('/search_data', methods=['POST'])
def display_search_data():
    """ Displays search groups and data on click for document owner """

    req = request.get_json()

    print(req, 'req!@--------------------------------------------^^')
    # search_phrase = "hey"

    search_phrase, doc_id = req

    print('-----------------------------^^^^^-----', type(doc_id))
    # user_id = session.get('user_id')
    # Will only be using this later when add more authentication
    # doc_id = 1

    file = Document.query.get(int(doc_id))

    searches = file.searches

    groups = []
    # create groups list

    for user_search in searches:
        if user_search.search_phrase == search_phrase:
            group = user_search.groups
            # get the group associated with the current search in the loop

            search_tuples = []
            # create search data list

            if group:
            # if group, if group belongs to current user

                search_phrase = user_search.search_phrase
                search_tuples.append(search_phrase)
                # append search_phrase

                matches = user_search.search_matches
                matches_list = []
                # create matches list

                search_tuples.append(matches_list)
                # append matches list to search data list

                for match in matches:
                    match_data = (match.match_content, match.match_id)
                    # create a tuple for each match containing the match_content and match_id)

                    notes = match.notes
                    # creates a list of match notes

                    content = []
                    # create a content list

                    content.append(match_data)
                    # add match_data tuple to content list

                    if notes:
                        note = (notes[0].note_content, notes[0].note_id)
                        # only be one note per match, but need to index because is a list
                        # create a tuple containing note_content and note_id

                        content.append(note)
                        # add note tuple to content list

                    content = tuple(content)
                    # make content list a tuple

                    matches_list.append(content)
                    # add content tuple to list of matches

                # search_tuples.append(matches_list)
                # add list of match content tuples to search data list
                # I believe I did this earlier, and this line is redundant

                search_tuples = tuple(search_tuples)
                # make search data list into a tuple

                groups.append(search_tuples)
                # add search data tuple of tuples of list of tuples into groups list

    # if not groups:
    #     flash('There are no saved groups')
        # this conditional should be set on front end
    print('GRUUUUP BEFORE', groups)

    groups = make_response(jsonify(groups))
    print(groups, '^^^^^^^^^^~~~~~~~~~~~~~~~~~GROUUUUUP')

    # resp = jsonify('this is a tuple', 1)

    return groups

    # ------------------------------------------------------------------------


@app.route('/upload_file')
def upload_document():
    """ Allows user to upload a document """

    return render_template("upload_file.html")


@app.route('/file_view', methods=['GET', 'POST'])
def display_document():
    """ Displays the document of user's choice """

    if request.method == 'POST':
    # upload_file uses post method to display this route, should not need post method otherwise

        file = request.files['file']
        # retrieves the uploaded file

        filename = request.form.get('filename')
        # gets the filename that was entered by the user

        end_number = random.randint(1, 268)
        start_number = random.randint(14,99)

        passcode = str(start_number) + secure_filename(filename[0:2]) + str(end_number)
        # create a passcode for the document

        doc_owner = request.form.get('documentowner')

        file = load_text(file, filename, passcode, doc_owner)
        # call load_text FN with the file and filename, add passcode and doc_owner

        user = create_user(doc_owner, file.document_id, True)
        # create a new user and set is_doc_owner to True

        session['user_id'] = user.user_id
        # store the user the session

        text = bytes.decode(file.text)
        # decodes byte string

        return render_template("file_view.html", file=file, text=text, passcode=passcode)
    
    if session.get('passcode'):
    # if session has passcode already stored
    # for users navigating to this view via link
    # not the most secure, will look into local storage to store this in the future

        doc_id = session.get('did')

        # user_id = session.get('user_id')
        # TODO: I'm not using this, so I don't think I need it here

        file = Document.query.get(doc_id)

        text = bytes.decode(file.text)
        # decodes byte string

        return render_template("file_view.html", file=file, text=text)

    else:
    # for users attempting to view document via given url and passcode

        doc_id = request.args.get('did')

        session["did"] = doc_id
        # store document user is trying to access in session to pass to /authenticate route

        return redirect('/authenticate')


@app.route('/search_view')
def search_document():
    """ Gets and stores user's input search on the given document """

    search_phrase = request.args.get('search_phrase')
    # gets the search phrase that was entered by the user

    document_id = request.args.get('doc_id')

    search_id = store_search(search_phrase, document_id)
    # calls FN to store search

    file = Document.query.get(document_id)
    text = bytes.decode(file.text)

    matches = search(search_phrase, text)
    # calls FN to regex over given phrase and decoded text
    # could decode within the search FN, looking into encrypting this document in the future

    return render_template("file_view.html", file=file, text=text, 
        search_phrase=search_phrase, search_id=search_id, matches=matches)


@app.route('/save_grouped_matches', methods=['POST'])
def save_matches():
    """ Saves the matches and notes in a group """

    req = request.get_json()
    # receive json data

    user_id = session.get('user_id')
    search_id = req['search_id']

    group_id = create_group(search_id, user_id)
    # call FN to create group using data received

    for match in req['matches']:

        start_offset = match['start_offset']
        end_offset = match['end_offset']
        match_content = match['match_content'][2:]
        # this is to strip off the x for now, still testing
        print('matchhhh', match_content)
        # TODO: remove this print

        match_id = store_match(search_id, start_offset, end_offset, match_content)
        # call FN to store each saved match result

        if match['notes']:
            note_content = match['notes']
            store_notes(note_content, match_id, group_id)
            # call FN to store saved notes per match

    # TODO: this flash message is currently not working, just mocked out for now
    flash('Your search matches and notes have been saved', 'info')
    
    res = make_response(jsonify("Success: True"), 200)
    # send success response to fetch

    return res


# -------------------------- UNDER CONSTRUCTION --------------------------
# route not working yet
@app.route('/update_grouped_matches', methods=['POST'])
def update_matches():
    """ Updates the matches and notes in a group """

    req = request.get_json()

    # for now, let's just update the note content according to match_id

    print('This is json from front end!!', req)

    search_id = req['search_id']
    # group_id = create_group(search_id)

    for match in req['matches']:

        start_offset = match['start_offset']
        end_offset = match['end_offset']
        match_content = match['match_content']

        # match_id = store_match(search_id, start_offset, end_offset, match_content)

        if match['notes']:
            note_content = match['notes']
            # store_notes(note_content, match_id, group_id)

    # this flash message is currently not working, just mocked out for now
    flash('Your search matches and notes have been saved')
    

    res = make_response(jsonify(req), 200)

    return res
# -------------------------------------------------------------------------


@app.route('/authenticate')
def get_passcode():
    """ Renders passcode authentication template upon redirect with static url """

    return render_template('enter_passcode.html')


@app.route('/authenticate', methods=['POST'])
def authenticate_passcode():
    """ Processes the given passcode."""

    username = request.form["username"]
    passcode = request.form["passcode"]

    doc_id = session.get('did')

    file = Document.query.get(doc_id)

    if file.passcode != passcode:
    # check if passcode given is the stored passcode for the requested document

        flash("Passcode is incorrect")
        return redirect("/authenticate")

    newuser = request.form.get('newuser')
    # has the user checked the newuser box?

    if newuser:
        user = create_user(username, doc_id)
        # call FN to create new user
        
    else:
        user = User.query.filter_by(username=username).first()
        # if not a new user, get the user object stored
        # does not account for repeat name entries yet

    session["user_id"] = user.user_id
    session["passcode"] = file.passcode
    # store the session data

    flash(f'Welcome, {username}')
    return redirect("/file_view")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')