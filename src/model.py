from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------- Model Definitions ----------

class Document(db.Model):

class Search(db.Model):

class Search_Match(db.Model):


# ----------- Helper Functions ------------

# def init_app():
#     """Makes Flask app to use Flask SQL Alchemy"""

#     from flask import Flask
#     app = Flask(__name__)

# this creates a Flask app on the model.py file, but we want one on the 
# server.py file

def connect_to_db(app):
    """Connects db to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgress:///searchy'

    # I'm not convinced we need these ---------------------------
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # -----------------------------------------------------------

    db.app = app

    db.init_app(app)


if __name__ == "__main__":

    from server.py import app
    connect_to_db(app)
    # run the module interactively to work with db directly
    print('Connected to DB')