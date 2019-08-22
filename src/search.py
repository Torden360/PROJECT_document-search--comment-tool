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


    context = re.findall(r'.*.*?[.?!]+.*{}.*?[.?!]+.*.*?[.?!]+'.format(phrase), text)

    # (match any character including newline, 
    # 0 or more of the previous char, 
    # then match the word, 
    # then match any char including \n, 
    # 0 or more of prev char, 
    # match 0 or 1 of the prev char, )
    # match any of these chars [.?!] - can do [^9] to match any char except 9
    # match 1 or more of the prev char
    # match any char include \n
    # match 0 + of the prev char
    # repeat the last 2 matches
    # match 0 or 1 of prev char
    # match the chars in set
    # match 1 or more of the chars in the set

    print('context!! ', context)


    multi = re.findall(r'.*{}.*?[.?!]+.*.*?[.?!]+'.format(phrase), text, re.MULTILINE & re.DOTALL)
    # multi = re.MULTILINE(r'.*{}.*?[.?!]+.*.*?[.?!]+'.format(phrase), text)

    print('multi ----- ', multi)

    some_before = re.findall(r'.*[.?!]*{}.*?[.?!]+'.format(phrase), text, re.DOTALL) #MULTILINE) # & re.DOTALL)
    # this is giving way too much. 

    print('SOME BEFOREEEE : ', some_before)

    some_after = re.findall(r'{}.*?[.?!]+.*?[.?!]+'.format(phrase), text, re.MULTILINE | re.DOTALL)
    # currently this is giving the sentences that include the word and a sentence after. Not the sentence before. It includes
    # the \n but I think I'll be able to take that out with styling and/or strip
    # it's mainly the DOTALL that is doing this, not positive I need the MULTILINE

    # although, I think I will want to include re.IGNORECASE
    # I also need to add boundaries

    # (\S+)\s*
    # put this in front, gets the word before 

    print('SOME AFTERRRRRRRR: ', some_after)


    # [^.?!]\s*(.)*?(\S+)*[.?!]+?\s*(Hey).*?[.?!]+.*?[.?!]+
    # Whaaat?

    context_notfirst = re.findall(r'[^.?!]\s*.*?(?:\S+)*[.?!]+?\s*\b{}\b.*?[.?!]+.*?[.?!]+'.format(phrase), text)

    # OMG THIS WORKS!!! Except, not for the first Hey -- and only for 'Hey' lol
    # becauuuuse it's finding based on the more than one spaces before/the newlines

    print('WHAAAAAAATTTTT:  ', context_notfirst)


    try_again = re.findall(r'[^.?!]*?[.?!]+.?\bHey\b.*?[.?!]+.*?[.?!]+', text, re.IGNORECASE)
    # for some reason, this works in the online py regex translator

    print("")
    print(try_again)
    for match in try_again:
        print('try AGAINNNNN ', match)
    print("")

    # don't understand why this doesn't work, but the online one does.
    # and actually, it's just matching on words that are the first word after a sentence

    # return match

    # this is what the working code online says:
    # coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

    regex = r"[^.?!]*?[.?!]+.?\bHey\b.*?[.?!]+.*?[.?!]+"

    test_str = ("Hey there,\n"
        "Here's a plain text page for you to read in and search then comment on... Today is nice and sunny, but last week was cold and dreary. Weather in San Francisco Normally it is cold at night, but because yesterday was sunny, it was kind of warm. Therefore, tonight may also be warm. Thank you for listening! Hey, have you ever been to Chicago? Neither have I. I hear it is quite windy there. Oh, boy!\n"
        "It's still quite windy in SF. There is also fog.")

    matches = re.finditer(regex, test_str, re.MULTILINE | re.IGNORECASE)

    for matchNum, match in enumerate(matches, start=1):
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

    # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.


def get_context(location):

    #return context
    pass


def search(phrase, document):

    pass
    # open_doc(document)

    # location = get_location(phrase)

    # context = get_context(phrase)

    # return f'The {phrase} is located {location} with context {context}'

