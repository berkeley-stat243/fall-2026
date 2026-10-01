I am working with an sqlite database of information on questions and answers on Stack Overflow. The information contained is the metadata without the full question or answer text. Each question is tagged with one or more keywords (tags) that indicate the topic of the question. There are four tables, with their fields indicated below:

questions: questionid, score, viewcount, title, ownerid
answers: questionid, answerid, ownerid, score
users: userid, creationdate, location, reputation, displayname, upvotes, downvotes
questions_tags: questionid, tag

questionid is a foreign key in questions_tags for questionid in questions
questionid is a foreign key in answers for questionid in questions
ownerid is a foreign key in questions for userid in users
ownerid is a foreign key in answers for userid in users
