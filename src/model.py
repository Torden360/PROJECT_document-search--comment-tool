from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------- Model Definitions ----------

class Document(db.Model):
    """ Uploaded document """

    __tablename__ = "documents"

    document_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(60))

    def __repr__(self):

        return f'<document_id = {self.document_id} name = {self.name}>'


class Search(db.Model):
    """ Search on document """

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_phrase = db.Column(db.String(150), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))

    def __repr__(self):

        return f'<search_id={self.search_id} search_phrase={self.search_phrase} document_id={self.document_id}>'


class Search_Match(db.Model):
    """ Search match / results found """

    __tablename__ = "search_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))
    start_offset = db.Column(db.Integer, nullable=False)
    end_offset = db.Column(db.Integer, nullable=False)


# ----------- Add After MVP ------------


# class Group(db.Model):

#     __tablename__ = "groups"

#     group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))


# class Group_Match(db.Model):

#     __tablename__ = "group_members"

#     member_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
#     search_match_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))


# class Comment(db.Model):

#     __tablename__ = "comments"


# ----------- Helper Functions ------------

# def init_app():
#     """Make Flask app to use Flask SQL Alchemy"""

#     from flask import Flask
#     app = Flask(__name__)

# this creates a Flask app on the model.py file, but we want one on the 
# server.py file


def connect_to_db(app):
    """Connect db to the Flask app"""

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