from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, jsonify, make_response, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

from werkzeug.utils import secure_filename

from sqlalchemy import func, distinct

from db_functions import load_text, store_search, create_group, store_match, store_notes

from search import search


ALLOWED_EXTENSIONS = {'txt'}
# not sure that I will use this/if I need it when I am forcing the accept params
# on the html itself. Which is better to do that with?/More secure

app = Flask(__name__)

app.secret_key = "ABC"


@app.route('/')
def display_user_homepage():
    """ Displays homepage """

    file = Document.query.get(3)

    return render_template('user_homepage.html', file=file)


@app.route('/user_groups')
def display_groups():
    """ Displays user's groups """

    file = Document.query.get(3)
    # testing this for now -- will remove once satisfied with results of db queries

    searches = file.searches

    groups = []

    for user_search in searches:
        group = user_search.groups
        search_tuples = []

        if group:
            search_phrase = user_search.search_phrase
            search_tuples.append(search_phrase)

            matches = user_search.search_matches
            matches_list = []
            search_tuples.append(matches_list)

            for match in matches:
                match_content = match.match_content
                notes = match.notes
                content = []

                content.append(match_content)

                if notes:
                    note = notes[0].note_content
                    content.append(note)

                content = tuple(content)
                matches_list.append(content)
            print('this is content: ', content)
            print('')

            search_tuples.append(matches_list)
            search_tuples = tuple(search_tuples)

            groups.append(search_tuples)

        print('this is matches list: ', matches_list)
    print('')
    print('this is the groups list: ', groups)

    groups = jsonify(groups)

    return groups


@app.route('/owner_home')
def display_document_owner_homepage():
    """ Displays the document of user's choice """

    file = Document.query.get(3)

    text = bytes.decode(file.text)
    # decodes byte string

    return render_template("owner_homepage.html", file=file, text=text)


@app.route('/stats_view')
def display_doc_stats():
    """ Displays document statistics for document owner """

    file = Document.query.get(3)
    searches = file.searches
    search_phrase_set = set()
    search_tuples = []

    for search_obj in searches:
        search_phrase_set.add(search_obj.search_phrase)
    
    for search_phrase in search_phrase_set:
        searches_w_phrase = Search.query.filter(Search.search_phrase==search_phrase).all()
        count = len(searches_w_phrase)
        search_tuple = (search_phrase, count)
        search_tuples.append(search_tuple)

    def Sort_Tuple(tup):  
   
        return(sorted(tup, key = lambda x: x[1], reverse=True))   

    search_tuples = Sort_Tuple(search_tuples)

    print('sorted : ', search_tuples)
    
    return render_template('stats_view.html', file=file, search_tuples=search_tuples)


@app.route('/upload_file')
def upload_document():
    """ Allows user to upload a document """

    return render_template("upload_file.html")


@app.route('/file_view', methods=['POST'])
def display_document():
    """ Displays the document of user's choice """

    file = request.files['file']
    # retrieves the uploaded file

    filename = request.form.get('filename')
    # gets the filename that was entered by the user

    file = load_text(file, filename)
    # call load_text FN with the file and filename

    text = bytes.decode(file.text)
    # decodes byte string

    return render_template("file_view.html", file=file, text=text)



# developping this in the most basic/redundant way for now

@app.route('/search_view')
def search_document():
    """ Gets and stores user's input search on the given document """

    search_phrase = request.args.get('search_phrase')
    # gets the search phrase that was entered by the user

    document_id = request.args.get('doc_id')

    search_id = store_search(search_phrase, document_id)

    file = Document.query.get(document_id)
    text = bytes.decode(file.text)

    matches = search(search_phrase, text)

    return render_template("file_view.html", file=file, text=text, 
        search_phrase=search_phrase, search_id=search_id, matches=matches)


# This route is incomplete
@app.route('/save_grouped_matches', methods=['POST'])
def save_matches():
    """ Saves the matches and notes in a group """

    req = request.get_json()

    print('This is json from front end!!', req)

    search_id = req['search_id']
    group_id = create_group(search_id)

    for match in req['matches']:

        start_offset = match['start_offset']
        end_offset = match['end_offset']
        match_content = match['match_content']

        match_id = store_match(search_id, start_offset, end_offset, match_content)

        if match['notes']:
            note_content = match['notes']
            store_notes(note_content, match_id, group_id)

    # this flash message is currently not working, just mocked out for now
    flash('Your search matches and notes have been saved')
    

    res = make_response(jsonify(req), 200)

    return res



if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')