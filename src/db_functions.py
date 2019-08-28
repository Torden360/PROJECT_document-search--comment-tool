from model import (Document, Search, Search_Match, connect_to_db, db) 

def load_text(document, name):
        """ Load the text from the document into database, and create new db object """

        text = document.read()

        document = Document(text=text,
                            name=name, 
                            )

        db.session.add(document)

        db.session.commit()

        return document


def store_search(search_phrase, document_id):
    """ Store search information into the database """


    search = Search(search_phrase=search_phrase,
                    document_id=document_id)

    db.session.add(search)
    db.session.commit()


def store_match(search_id, start_offset, end_offset):

    match = Search_Match(search_id=search_id,
                  start_offset=start_offset,
                  end_offset=end_offset)

    db.session.add(match)
    db.session.commit()

