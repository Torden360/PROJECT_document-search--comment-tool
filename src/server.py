from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

from werkzeug.utils import secure_filename

from sqlalchemy import func


ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)

app.secret_key = "ABC"


# mocking out server.py for now


def load_text(document, name):
        """ Load the text from the document into database """

        text = document.read()

        document = Document(text=text,
                            name=name, 
                            )

        db.session.add(document)

        db.session.commit()

        return document


@app.route('/')
def display_homepage():
    """ Displays homepage """

    file = Document.query.get(1)
    # testing this for now -- will remove once satisfied with results of db queries

    return render_template('homepage.html', file=file)


@app.route('/upload_file')
def upload_document():
    """ Allows user to upload a document """

    return render_template("upload_file.html")


@app.route('/file_view', methods=['POST'])
def display_document():
    """ Displays the document of user's choice """

    file = request.files['file']

    filename = request.form.get('filename')
    filename = secure_filename(filename)

    file = load_text(file, filename)

    return render_template("file_view.html", file=file)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')