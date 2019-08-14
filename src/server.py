from Jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Document, Search, Search_Match, Group, Group_Match,
 connect_to_db, db)

 app = Flask(__name__)