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
# why doesn't this work? compared to def search I know why. it's because the . is not the special char, when it's in a group like that,
# it's escaped
    matches = re.finditer(r'[^.]*[.(?:\s)]*[^.]*(\b{}\b)[^.]*[.(?:\s)]*[^.]*[.(?:\s)]'.format(phrase), document_text, re.IGNORECASE)
    # this works great! except, if the word match is in the same sentence, it only returns one
    # match/comment box. And, seems like a lot of work/takes a long time in a large file like Hamlet
    # print(matches.values())
    # print(matches.end)

    for match in matches:
        print('match.groups: ', match.groups())
        print('match.group: ', match.group(), match.start(), match.end()) #, document_text[int(f'{match.start})':int(f'{match.end}')])
    return matches


def search(phrase, document_text):

    # phrase = re.escape(phrase)
    # This is escaping, but then the for loop doesn't work
    matches = re.finditer(r'[^.?!]*[.?!(?:\s)]*[^.?!]*\b({})\b[^.?!]*[.?!(?:\s)]*[^.?!]*[.?!(?:\s)]'.format(phrase), document_text, re.IGNORECASE)
    print('this be matches:', matches)
    matches_list = []
    for match in matches:
        print('this be match', match)
        print(match.start(1), match.end(1), 'trying to get diff index', match.end())
        print(match.span(1), 'we shall see')
        match_dict = {}
        match_gr = match.group()
        match_dict['match'] = match_gr.replace('\n', ' ')
        match_dict['start'] = [match.start(1), match.start()]
        match_dict['end'] = [match.end(1), match.end()]
        matches_list.append(match_dict)
        print('arrrrrrrrr')

    print(matches_list, 'this is matches list')
    return matches_list

    # This is not working properly, is not matching on last word tomorrow:
    # search('hey', '''hey this is so much fun today i felt like. i just knew. there was going to be. a day someday somehwere. somehow. there's always a day awayyyyyyyy. tomorrow ! tomorrow ! i lov ya. hey, tomorrow''')
    # this is match.groups:  ('hey',)
    # this is match.group:  hey this is so much fun today i felt like. i just knew.
    # this is match.groups:  ('hey',)
    # this is match.group:   i lov ya. hey,
    # <callable_iterator object at 0x10e336f98>

    # open_doc(document)

    # location = get_location(phrase)

    # context = get_context(phrase)

    # return f'The {phrase} is located {location} with context {context}'

