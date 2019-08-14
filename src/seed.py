from sqlalchemy import func
from model import (Document, Search, Search_Match, connect_to_db, db)
from server import app

# may or may not use the following in this file:
import datetime
import re

def load_text(document):
    """ Load the text from the document into database """

    Document.query.delete()
    # delete existing documents so we don't get an error when running this file
    # multiple times

    open(document)
    # I swear there's another way to open a file without having to close it--have
    # to look for that tonight. 

    name = (document)
    text = read(document)

    document = Document(name=name, 
                        text=text
                        )

    db.session.add(Document)

    db.session.commit()

    close(document)


def store_search(search):
    """ Store search information into the database """


    search = Search(search_phrase=search_phrase,
        

    db.session.add(Search)
    db.session.commit()

