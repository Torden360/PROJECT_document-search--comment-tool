from sqlalchemy import func
from model import (Document, Search, Search_Match, connect_to_db, db)
from server import app

# may or may not use the following in this file:
import datetime
import re

def load_text(document, name):
    """ Load the text from the document into database """

    # Document.query.delete()
    # delete existing documents so we don't get an error when running this file
    # multiple times
    # on second thought, I don't think I'll run this file as itself, but import 
    # FNs to other files from it

    document = open(document)
    # I swear there's another way to open a file without having to close it--have
    # to look for that tonight. 

    # name = (document)
    # Having user input name
    
    text = document.read()

    document = Document(name=name, 
                        text=text
                        )

    db.session.add(document)

    db.session.commit()

    document.close()


def store_search(search, document_id):
    """ Store search information into the database """


    search = Search(search_phrase=search_phrase,
                    document_id=document_id)




    db.session.add(search)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_text('text_page.html')