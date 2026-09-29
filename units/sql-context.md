I am working with an sqlite database of information on questions and answers on Stack Overflow. The information contained is the metadata without the full question or answer text. There are four tables, with their fields indicated below:

questions: questionid, score, viewcount, title, ownerid
answers: questionid, answerid, ownerid, score
users: userid, creationdate, location, reputation, displayname, upvotes, downvotes
tags: questionid, tag
