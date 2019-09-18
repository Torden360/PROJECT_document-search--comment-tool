from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy_utils import PasswordType, force_auto_coercion
# TODO: don't think I need to import func here

db = SQLAlchemy()
force_auto_coercion()

# ----------- Model Definitions ----------

class Document(db.Model):
    """ Uploaded document """

    __tablename__ = "documents"

    document_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.LargeBinary, nullable=False)
    # db.LargeBinary stores the file in a bytea column, sqlalchemy takes care of conversion
    name = db.Column(db.String(60))
    passcode = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512'
        ]
    ))
    # TODO: make passcode a passwordType
    doc_owner = db.Column(db.String(60), nullable=False)
    # I would want to do this instead for more security, but don't have time to build out the other functionalities it requires
    # owner_id = db.Column(db.Integer, db.ForeignKey('document_users.user_id') nullable=False)

    def __repr__(self):

        return f'<document_id = {self.document_id} name = {self.name}>'


class User(db.Model):
    """ Document users """

    __tablename__ = "document_users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))
    is_doc_owner = db.Column(db.Boolean)

    document = db.relationship('Document', backref='document_users')
    group = db.relationship('Group', backref='document_users')

    def __repr__(self):

        return f'<document_id = {self.document_id} name = {self.username}>'


class Search(db.Model):
    """ Search on document """

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_phrase = db.Column(db.String(150), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))

    document = db.relationship('Document', backref='searches')
    group = db.relationship('Group', backref="searches")

    def __repr__(self):

        return f'<search_id={self.search_id} search_phrase={self.search_phrase} document_id={self.document_id}>'


class Search_Match(db.Model):
    """ Search match / results found """

    __tablename__ = "search_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))
    start_offset = db.Column(db.String(150), nullable=False)
    end_offset = db.Column(db.String(150), nullable=False)
    match_content = db.Column(db.Text)

# TODO: think I will need to add group member_id, group_id

    search = db.relationship('Search', backref='search_matches')

# TODO: add __repr__


# ----------- Add After MVP ------------

class Group(db.Model):

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'), nullable=False)
    # match_id = db.Column(db.Integer, db.ForeignKey('search_matches.match_id'))
    # TODO: not sure if I want match_id here
    user_id = db.Column(db.Integer, db.ForeignKey('document_users.user_id'), nullable=False)
    # TODO: need to add user_id to instantiate fn and to input variables

    search = db.relationship('Search', backref='groups')
    user = db.relationship('User', backref='groups')

#TODO: I forgot to add group_id to search_matches + relationship, and I'm payin' for it.

# TODO: add __repr__


# TODO: think I will get rid of this table--DO NOT DELETE UNTIL COMPLETE DB
# class Group_Match(db.Model):

#     __tablename__ = "group_members"

#     member_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
#     search_match_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))


class Note(db.Model):

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note_content = db.Column(db.Text)
    match_id = db.Column(db.Integer, db.ForeignKey('search_matches.match_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    match = db.relationship('Search_Match', backref='notes')
    group = db.relationship('Group', backref='notes')

    # TODO: add __repr__


# ----------- Helper Functions ------------

# def init_app():
#     """Make Flask app to use Flask SQL Alchemy"""

#     from flask import Flask
#     app = Flask(__name__)

# this creates a Flask app on the model.py file, but we want one on the 
# server.py file


def connect_to_db(app):
    """Connect db to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///searchy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # should turn this off, otherwise buggy

    app.config['SQLALCHEMY_ECHO'] = True
    # don't need to have this on, unless want to see the SQL query that 
    # sqlalchemy is executing

    db.app = app

    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    # run the module interactively to work with db directly
    
    print('Connected to DB')

    db.create_all()