from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# TODO: don't think I need to import func here

db = SQLAlchemy()

# ----------- Model Definitions ----------

class Document(db.Model):
    """ Uploaded document """

    __tablename__ = "documents"

    document_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.LargeBinary, nullable=False)
    # db.LargeBinary stores the file in a bytea column, sqlalchemy takes care of conversion
    name = db.Column(db.String(60))

    def __repr__(self):

        return f'<document_id = {self.document_id} name = {self.name}>'


class Search(db.Model):
    """ Search on document """

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_phrase = db.Column(db.String(150), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))
    # TODO: will probably add count later to store num times phrase was searched

    document = db.relationship('Document', backref='searches')

    def __repr__(self):

        return f'<search_id={self.search_id} search_phrase={self.search_phrase} document_id={self.document_id}>'


class Search_Match(db.Model):
    """ Search match / results found """

    __tablename__ = "search_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))
    start_offset = db.Column(db.Integer, nullable=False)
    end_offset = db.Column(db.Integer, nullable=False)
# TODO: think I will need to add group member_id, group_id

    search = db.relationship('Search', backref="search_matches")


# ----------- Add After MVP ------------


# class Group(db.Model):

#     __tablename__ = "groups"

#     group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))

# TODO: think I will get rid of this table--DO NOT DELETE UNTIL COMPLETE DB
# class Group_Match(db.Model):

#     __tablename__ = "group_members"

#     member_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
#     search_match_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))


# class Comment(db.Model):

#     __tablename__ = "comments"

    # note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # note_content = db.Column(db.Text)
    # group_id = db.Column(db.Integer, nullable=False, db.ForeignKey('groups.group_id'))
    # TODO: I see, I do need a match ID here. 

    # search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'))
    # TODO: search_id may not be necessary here


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