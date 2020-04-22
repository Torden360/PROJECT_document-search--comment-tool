# SearchUse

Author: Tyler Ordenstein

## Overview

Hi, my name is Tyler, I’m native Hawaiian and I had BIG dreams of leaving home and becoming a TV/movie producer. So, I have a degree in it.‍ And although I’m now looking forward to applying my past experience to a Site Reliability or Backend Engineering role, I still have quite a few friends asking me for feedback on their novels and screenplays. 

And I LOVE giving feedback. So much, in fact, that I created an app to address the needs that I've had when going through this process. 

Think: Google Docs, but with the ability to link comments in different parts of the file to one another. I wanted my notes to have `relationship`,
`surrounding context` of each instance within that relationship to further connect the dots, and
`statistics`, to show how frequently contributors are looking at the same issue.

Upon document upload, I store the file in a byte array inside a PostgreSQL database, the file view is very minimal. 

Searches are stored with unique IDs to prevent any session collisions, to allow for multiple saves per search phrase, and to be collected for statistics. 

Users are able to X out of matches, add notes, and preserve relationships with save.

I'm using JavaScript and fetch to listen to events and send JSON data back to Flask. 

Users may update their own saves, document owners may view all saves and all statics per document. 

Using Regex, I retrieve what I call ‘context’ which is the sentence containing, the sentence before, and the sentence after. 

While creating my Regex, I came across several issues: one of which was optimization. Initially, I wondered if using another language, such as Perl would decrease runtime. With research, I found that those optimizations would likely be minimal. 

Enter, Nondeterministic finite automaton (NFA), I'm hoping to convert my Regex into an NFA, an abstract machine that functions to change Regex’s exponential runtime into a faster, linear runtime for larger content.

Especially with some of the uploaded data being potentially sensitive, I would like to take security seriously. Currently, my app generates a unique pass-code per document, hashed in the database, which the owner can then share with their circle to access a static URL. However, I want to get to the point where my server never sees an unencrypted version of the file, potentially using a public/private key encryption with local storage. I want authors to be able to trust that my app will respect their work.
