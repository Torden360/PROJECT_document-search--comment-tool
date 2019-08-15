from Jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, connect_to_db, db) 
# will add Group, Group_Match, and Comment after MVP

app = Flask(__name__)

app.secret_key = "ABC"

# mocking out server.py for now

@app.route('/document')
def upload_document():
    """ Allows user to upload a document """

    return render_template("upload_document.html")


@app.route('/document/{id}')
def display_document():
    """ Displays the document of user's choice """

    return render_template("document_{id}.html")
