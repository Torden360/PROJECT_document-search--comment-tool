from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

from werkzeug.utils import secure_filename

from sqlalchemy import func

from db_functions import load_text


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

    filename = secure_filename(filename)
    # DOCUMENTATION says this ensures the filename is safe???
    # may not be necessary because this is mostly if you're saving a file to the file system

    file = load_text(file, filename)
    # call load_text FN with the file and filename

    text = bytes.decode(file.text)

    return render_template("file_view.html", file=file, text=text)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')