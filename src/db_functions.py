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


# def store_search(search, document_id):
#     """ Store search information into the database """


#     search = Search(search_phrase=search_phrase,
#                     document_id=document_id)




#     db.session.add(search)
#     db.session.commit()
