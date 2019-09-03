from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, jsonify, make_response, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

from werkzeug.utils import secure_filename

from sqlalchemy import func

from db_functions import load_text, store_search

from search import search


ALLOWED_EXTENSIONS = {'txt'}
# not sure that I will use this/if I need it when I am forcing the accept params
# on the html itself. Which is better to do that with?/More secure

app = Flask(__name__)

app.secret_key = "ABC"


@app.route('/')
def display_homepage():
    """ Displays homepage """

    file = Document.query.get(2)
    # testing this for now -- will remove once satisfied with results of db queries

    text = bytes.decode(file.text)

    return render_template('homepage.html', file=file, text=text)


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

    store_search(search_phrase, document_id)

    file = Document.query.get(document_id)
    text = bytes.decode(file.text)

    matches = search(search_phrase, text)

    return render_template("file_view.html", file=file, text=text, 
        search_phrase=search_phrase, matches=matches)


# This route is incomplete
@app.route('/save_grouped_matches', methods=['POST'])
def save_matches():
    """ Saves the matches and notes in a group """
    # probably should make this a post method

    req = request.get_json()

    print('This is json from front end!!', req)
    
    res = make_response(jsonify(req), 200)

    return res

#     search_phrase = request.args.get('search_phrase')
#     # gets the search phrase that was entered by the user

#     document_id = request.args.get('doc_id')

#     file = Document.query.get(document_id)
#     text = bytes.decode(file.text)

#     matches = search(search_phrase, text)
#     print(matches)

    # if request.args.get('save'):
    #     store_match(search_id, start_offset, end_offset)
    #     flash("Your Grouped Matches and Notes have been saved!")

    #return render_template("file_view.html", file=file, text=text,
        # search_phrase=search_phrase, matches=matches)




if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')