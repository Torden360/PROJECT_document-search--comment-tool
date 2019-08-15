from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

app = Flask(__name__)

app.secret_key = "ABC"

# mocking out server.py for now

@app.route('/')
def display_homepage():
    """ Displays homepage """

    return render_template('homepage.html')


@app.route('/upload_file')
def upload_document():
    """ Allows user to upload a document """

    return render_template("upload_file.html")


@app.route('/file_view', methods=['POST'])
def display_document():
    """ Displays the document of user's choice """

    file = request.form.get('file')
    filename = request.form.get('filename')

    print(filename)
    print(file)


    return render_template("file_view.html", filename=filename, file=file)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')