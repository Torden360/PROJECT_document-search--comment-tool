import re


def open_doc(document):
    document = open(document)

    text = document.read()

    return text


def get_location(phrase):

    document = open('text_page.html')

    text = document.read()

    print('phrase', phrase)
    print('text!:', text)

    match = re.findall(phrase, text)

    print(match)

    location = re.search(phrase, text)

    print('re.search', location)

    iter = re.finditer(phrase, text)

    for i in iter:
        print("this is iter:", 'start=', i.start(), 'end=', i.end(), i)

    return match


def get_context(location):

    #return context
    pass


def search(phrase, document):

    pass
    # open_doc(document)

    # location = get_location(phrase)

    # context = get_context(phrase)

    # return f'The {phrase} is located {location} with context {context}'

