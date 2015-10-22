# Introduction #

This Page provides links to available data.  So far, all EMO20Q data has been collected at [USC's Sail lab](http://sail.usc.edu), but we hope that others will join in the fun and share their data here as well.  As the project is underway, this site may be out of data from time to time. Please ask if you would like any additional information that you do not find on this site.


# Current Data: Raw and Annotated #

Currently, there are 104 matches which consist  of 1194 question-answer turns from 28 users.

  * [Raw, anonymized chat logs from svn](https://code.google.com/p/emotion-twenty-questions/source/browse/trunk#trunk%2Fanon_chatlogs)
  * [Annotated data in question-answer pairs](https://code.google.com/p/emotion-twenty-questions/source/browse/trunk#trunk%2Fannotate%2Femo20q.txt)


# Releases #

## Sqlite DB, 2011-10-23 (after ACII 2011) ##

Here is the [annotated data imported into sqlite database](https://emotion-twenty-questions.googlecode.com/svn/trunk/db/emo20q.db), which comprises 104 matches, 1194 question-answer turns, from 28 users/players.  For the db details (schema, examples, etc.) see [SqliteDb](SqliteDb.md)

## Post-quals, tournament with mainly SAIL lab players ##

This data is a larger data collection.  The goal was to get more players, more emotions, and more longitudinal interaction.  There are 21 users, disregarding the test users:

` ls anon_chatlogs | perl -e '$/="";$a=<>; (@b) = ($a =~ /\d{4}-\d{2}-\d{2}_(.+)_(.+).log$/gm);print $_, "\n" for @b;' | sort | uniq | wc `

there are 44 unique emotions that were picked in the 50 matches that were played.

  * [questions list](https://code.google.com/p/emotion-twenty-questions/source/browse/wiki/questionsWithCounts.tmp), [answers list](https://code.google.com/p/emotion-twenty-questions/source/browse/wiki/answersWithCounts.tmp),

## Pre-quals/dissertation-proposal pilot data (before May 17, 2011) ##

This data was the first data collected.  It was collected and annotated before May 17, 2011.  This phase can be seen as a pilot study: smaller in scope and subject to changes.  There were 12 players and 26 matches, 23 distinct emotions played (list).  This data is the data that resulted in Abe's dissertation proposal as well as the interspeech 2011 (Florence) paper, as well as another paper (under review).  the main in change to the rules was the addition of the rule about exact/indistinguishable synonyms.

  * Pre-quals/dissertation-proposal data: from interspeech and acii 2011 papers, annotated and annonymized is available [here](http://code.google.com/p/emotion-twenty-questions/downloads/detail?name=annotatedAnonimizedQAPairs_prequal20110306.txt)

  * matlab loadable adjacency matrix graph [here](http://emotion-twenty-questions.googlecode.com/svn/branches/prequal20110517/lists/features.txt).

  * data and scripts are saved as an svn branch http://emotion-twenty-questions.googlecode.com/svn/branches/prequal20110517/