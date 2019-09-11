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


def get_context(phrase, document_text):

    matches = re.finditer(r'[^.?!]*[.?!(?:\s)]*[^.?!]*\b({})\b[^.?!]*[.?!(?:\s)]*[^.?!]*[.?!(?:\s)]'.format(phrase), document_text, re.IGNORECASE)
    # this works great! except, if the word match is in the same sentence, it only returns one
    # match/comment box. And, seems like a lot of work/takes a long time in a large file like Hamlet
    print(matches.values())
    # print(matches.end)
    return matches


def search(phrase, document_text):

#     matches = re.findall(r'\b{}\b'.format(phrase), document_text)

    matches = re.findall(r'[^.?!]*[.?!(?:\s)]*[^.?!]*\b{}\b[^.?!]*[.?!(?:\s)]*[^.?!]*[.?!(?:\s)]'.format(phrase), document_text, re.IGNORECASE)

    return matches

    # open_doc(document)

    # location = get_location(phrase)

    # context = get_context(phrase)

    # return f'The {phrase} is located {location} with context {context}'

