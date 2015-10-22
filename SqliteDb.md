# Introduction #

Sqlite is a pretty useful file-based database.  Google it for more info.





# Details #

## Getting Started ##

To download the emo20q human-human data in sqlite format:

`wget https://emotion-twenty-questions.googlecode.com/svn/trunk/db/emo20q.db`

(or just download it manually from the [above url](https://emotion-twenty-questions.googlecode.com/svn/trunk/db/emo20q.db))

Coming from more standard databases, the sql in sqlite is slightly different.

Here is the database schema

`sqlite3 emo20q.db ".schema"`

the output is as follows (the text after "--" is comments):

```
CREATE TABLE answers (         -- keeps track of answers
        a VARCHAR NOT NULL,    -- answer text (primary key)
        gloss VARCHAR,         -- logical annotation of answer
        clean VARCHAR,         -- cleaned form of answer (using correct spelling, etc)
        t INTEGER,             -- truth-value associated with answer (currently empty)
        PRIMARY KEY (a)
);
CREATE TABLE matches (
        id INTEGER NOT NULL,   -- match id (primary key)
        answerer VARCHAR,      -- answerer player id
        questioner VARCHAR,    -- questioner player id
        line INTEGER,          -- line from chat log where match starts (currently empty)
        start VARCHAR,         -- start time
        "end" VARCHAR,         -- end time
        emotion VARCHAR,       -- emotion chosen by answerer in match
        outcome VARCHAR,       -- whether the questioner correctly guessed the emo or not
        PRIMARY KEY (id)
);
CREATE TABLE questions (
        q VARCHAR NOT NULL,    -- question text (primary key)
        gloss VARCHAR,         -- logical annotation of question 
        clean VARCHAR,         -- question with clean spelling/orthography
        qtmplt VARCHAR,        -- template for asking a question eg, 'Is {e} a positive emotion?'  (currently not used)
        atmplt VARCHAR,        -- template for making a statement, eg, '{e} is an emotion that you would feel if you stub your toe.'
        ptag VARCHAR,          -- the positive tag for an answer: eg, it is, it can, one can, etc.
        ntag VARCHAR,          -- the negative tag for an answer: it is not,  it cannot, etc
        PRIMARY KEY (q)
);
CREATE TABLE turns (           -- table for each q-a turn
        id INTEGER NOT NULL,   -- id 
        m INTEGER,             -- match id (foreign key)
        e VARCHAR,             -- emotion name
        q VARCHAR,             -- question text (foreign key, questions table)
        a VARCHAR,             -- answer text (foreign key, answers table)
        p INTEGER,             -- previous question (foreign key, turns table)
        n INTEGER,             -- next question (foreign key, turns table)
        PRIMARY KEY (id),
        FOREIGN KEY(m) REFERENCES matches (id),
        FOREIGN KEY(q) REFERENCES questions (q),
        FOREIGN KEY(a) REFERENCES answers (a),
        FOREIGN KEY(p) REFERENCES turns (id),
        FOREIGN KEY(n) REFERENCES turns (id)
);
```


## looking at the data ##

the follwing command will list off all the turns

`sqlite3 emo20q.db "select * from turns;"`

Oop's, I just noticed that some of the fields (m,match id, and e, emotion, are not being filled in... I'll fix that
-Abe