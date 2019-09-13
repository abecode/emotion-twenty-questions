#!/usr/bin/python

import os
import re
import json
#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()
#from sqlalchemy import Column, Integer, String, MetaData, create_engine, ForeignKey

class Tournament():
    def matches(self):
        return self._matches
    def __add__(self,other):
        t = Tournament()
        t._matches = []
        t._matches.extend(self.matches())
        t._matches.extend(other.matches())
        return t

class HumanComputerTournament(Tournament):
    """A set of emo20q matches played by a human and a computer"""
    def __init__(self, annotationFile=None):
        if not annotationFile:
            import os
            annotationFile = os.path.dirname(__file__) + "/onlineResults_2011-10-28.txt"
        f = open(annotationFile, 'rU')
        line = f.readline() #remove header
        try:
            self._matches = [m for m in self.readMatches(f)]
            #for m in self.getMatches(f):
            #    print m.turns[0]
        finally:
            f.close()
    def readMatches(self,fh):
        matches = []
        turns = []
        currentEmotion = ""
        for line in fh:
            turn = Turn()
            m = re.match("^(?P<emotion>.+?)\t(?P<stimuli>.+?)\t(?P<response>.+?)$", line)
            emotion = m.group('emotion').lower()
            turn.qgloss = m.group('stimuli')
            turn.a = m.group('response')
            if(emotion!=currentEmotion):
                mtch = Match()
                mtch._turns=turns
                mtch._emotion=currentEmotion
                if currentEmotion != '':       #there was a blank/empty emotion
                    matches.append(mtch)
                turns = []
                currentEmotion=emotion
            turns.append(turn)
        else:
            return matches

class HumanComputerCouchDbTournament(Tournament):
    """A set of emo20q matches played by a human and a computer, read from a
    couchdb database

    >>> t = HumanComputerCouchDbTournament()

    """
    # the previous commit was the real one...
    #def __init__(self, dbUrl="http://ark.usc.edu:5984/emo20q_webdata"):
    #def __init__(self, dbUrl="http://localhost:5984/emo20q_webdata"):
    def __init__(self, dbUrl="http://emo20q.iriscouch.com/emo20q_webdata"):
        import couchdb
        db = couchdb.client.Database(dbUrl)
        self._matches = []
        #for row in db.view('_design/mturk/_view/all'):
        for row in db.view('_all_docs', include_docs=True):
            mtch = Match()
            doc = db.get(row.key)
            if 'param' not in doc: continue #this is a design document, not data
            if 'emotion' not in doc['param']: continue # this this emo20q dialog hasn't been annotated
            if 'container' not in doc: raise KeyError('"container" not found in doc') #this shouldn't happen ever
            mtch._emotion = doc['param']['emotion']
            #print mtch._emotion
            mtch._turns = []
            for t in doc['container']:
                if 'type' in t and t['type'] == "Turn":
                    turn = Turn()
                    turn.qgloss= t['container'][0]['param']['gloss']
                    turn.a = t['container'][1]['param']['text']
                    #print turn.qgloss, turn.a
                    mtch._turns.append(turn)
            self._matches.append(mtch)


class HumanComputerCouchJsonTournament(Tournament):
    """A set of emo20q matches played by a human and a computer, read from a
    a json dump of a couchdb database

    >>> t = HumanComputerJsonTournament()

    """
    # the previous commit was the real one...
    def __init__(self, fname="/Users/kaze7539/proj/emo20q/emo20q_github/db/emo20q_webdata_fromCouch_20121102.json"):
        db = json.load(open(fname))
        self._matches = []
        for row in db.get("rows"):
            mtch = Match()
            doc = row.get('doc')
            if 'param' not in doc: continue #this is a design document, not data
            if 'emotion' not in doc['param']: continue # this this emo20q dialog hasn't been annotated
            if 'container' not in doc: raise KeyError('"container" not found in doc') #this shouldn't happen ever
            mtch._emotion = doc['param']['emotion']
            #print mtch._emotion
            mtch._turns = []
            for t in doc['container']:
                if 'type' in t and t['type'] == "Turn":
                    turn = Turn()
                    turn.qgloss= t['container'][0]['param']['gloss']
                    turn.a = t['container'][1]['param']['text']
                    #print turn.qgloss, turn.a
                    mtch._turns.append(turn)
            self._matches.append(mtch)



class HumanHumanTournament(Tournament):
    """A set of emo20q matches played by two humans"""

    def __init__(self, annotationFile=None):
#        self.base = Base()
        if not annotationFile:
            annotationFile = os.path.dirname(__file__) + "/emo20q.txt"
        f = open(annotationFile, 'rU')
        try:
            self._matches = [m for m in self.readMatches(f)]
            #for m in self.getMatches(f):
            #    print m.turns[0]
        finally:
            f.close()

    def readMatches(self,fh):
        matches = []
        while True:
            line = fh.readline()
            if not line:
                break
            mtch = Match()
            turns = []
            if re.match("match:\d+", line):
                m = re.match("match:\d+, answerer:(?P<answerer>.+?), questioner:(?P<questioner>.+?), start:\"(?P<start>.+?)\"", line)
                mtch.answerer = m.group('answerer')
                mtch.questioner = m.group('questioner')
                mtch.start = m.group('start')
                #for turn in self.getTurns(fh):
                #    print turn
                turns = [turn for turn in mtch.readTurns(fh)]
                line = fh.readline()
                #print "should say end: " + line
                m = re.match("end:\"(?P<end>.+?)\", emotion:(?P<emotion>.+?), questions:(?P<questions>.+?), outcome:(?P<outcome>.+)(, .*)?",line)
                mtch._end = m.group('end');
                mtch._emotion = m.group('emotion');
                mtch._questions = m.group('questions');
                mtch._outcome = m.group('outcome');
                mtch._turns = turns
                #print mtch._emotion
                yield(mtch)

    #def createSqliteDb(self,engine):
        #engine = create_engine('sqlite:///emo20q.db', echo=True)
        #self.base.metadata.create_all(engine)


    def printStats(self):
        print("there are {0:d} matches".format(len(t.matches)))
        #sum up the turns
        sumTurns = 0
        for m_idx,m in enumerate(t.matches):
            assert isinstance(m,Match)
            assert type(m._turns) == list
            print("  In match {0:d} there are {1:d} turns.".format(m_idx,len(m.turns)))
            for tn_idx,tn in enumerate(m.turns()):
                assert isinstance(tn,Turn)
                #further tests
                sumTurns = sumTurns + len(m.turns())

        print("In all, there are {0:d} turns.".format(sumTurns))


#class Match(Base):
class Match(object):
    """An emo20q game instance"""

    #the following is sqlalchemy stuff
    # __tablename__ = "matches"
    # id = Column(Integer, primary_key=True)
    # answerer = Column(String)
    # questioner = Column(String)
    # line = Column(Integer)
    # start = Column(String)
    # end = Column(String)
    # emotion = Column(String)
    # outcome = Column(String)

    def turns(self):
        return self._turns
    def emotion(self):
        return self._emotion



    def readTurns(self,fh):
        while True:
            turn = Turn()
            question = ""
            answer   = ""
            qgloss   = ""
            agloss   = ""
            while True:
                line = fh.readline()
                #print "question: "+line
                if not line:
                    break
                if re.match("end:", line):
                    fh.seek(fh.tell() - len(line.encode("utf-8")),
                            os.SEEK_SET)
                    return
                if re.match("^ *$",line):
                    continue
                elif re.match("gloss:",line):
                    m = re.match("gloss:{(.*)}",line)
                    qgloss = m.group(1)
                    break
                else:
                    question += line

            while True:
                line = fh.readline()
                #print "answer: "+line
                if not line:
                    break
                if re.match("end:",line):
                    fh.seek(-len(line),1)
                    break
                if re.match("-", line):
                    continue
                elif re.match("gloss:",line):
                    m = re.match("gloss:{(.*)}",line)
                    agloss = m.group(1)
                    break
                else:
                    answer += line

            turn.q = question.strip()
            turn.qgloss = qgloss.strip()
            turn.a = answer.strip()
            turn.agloss = agloss.strip()
            #ignore non-yes-no questions and their answers
            if "non-yes-no" in turn.agloss: continue
            if "non-yes-no" in turn.qgloss: continue
            yield turn

#class Turn(Base):
class Turn(object):
    """One of the question/answer pairs from and emo20q match"""

    #sqlalchemy stuff
    # __tablename__ = "turns"
    # id = Column(Integer, primary_key=True)
    # m = Column(Integer, ForeignKey('matches.id')) #match id
    # e = Column(String)  #emotion
    # q = Column(String, ForeignKey('questions.q'))  #question string
    # a = Column(String, ForeignKey('answers.a'))  #answer   string
    # p = Column(Integer, ForeignKey('turns.id')) #previous turn id
    # n = Column(Integer, ForeignKey('turns.id')) #next turn id

    def questionId(self):
        return self.qgloss
    def answerId(self):
        ans = "other"
        if "agloss" in self.__dict__:
            if self.agloss.find("yes") == 0 : ans = "yes"
            if self.agloss.find("no") == 0 : ans = "no"
        else:
            if self.a.lower().find("yes") == 0 : ans = "yes"
            if self.a.lower().find("no") == 0 : ans = "no"

        return ans

#class Question(Base):
class Question(object):
    """Keeps track of question strings"""

    # #sqlalchemy stuff
    # __tablename__ = "questions"
    # q = Column(String, primary_key=True)
    # gloss = Column(String)  #question's logical gloss
    # clean = Column(String)  #a cleaned verson of the question, ei, correct orthography
    # qtmplt = Column(String)  #question's template
    # atmplt = Column(String)  #question's answer template, eg, declarative form
    # ptag = Column(String)   #yes + [it is, it does, you can, it can, one can, etc]
    # ntag = Column(String)   #no + [it is not it does not, it can't, etc]

    def __init__(self,q,gloss):
        self.q = q
        self.gloss = gloss

#class Answer(Base):
class Answer(object):
    """Keeps track of answer strings"""

    # #sqlalchemy stuff
    # __tablename__ = "answers"
    # a = Column(String, primary_key=True)
    # gloss = Column(String)  #question's logical gloss
    # clean = Column(String)  #a cleaned verson of the question, ei, correct orthography
    # t = Column(Integer)     #truth degree

    def __init__(self,a,gloss):
        self.a = a
        self.gloss = gloss



if __name__ == "__main__":

    import argparse
    argParser = argparse.ArgumentParser(description="""A generalized pushdown automaton implementation of an EMO20Q questioner agent.  """)
    argParser.add_argument('-t', '--test',
                           action='store_true',
                           help='test using doctest')
    argParser.add_argument('--run',
                           action='store_true',
                           help='do some random stuff... nothing very useful, just some print statments and networkx plot')

    args = argParser.parse_args()
    if args.test:
        import doctest
        doctest.testmod()
    elif args.run:  #just some random stuff

        # read in tournament, do some testing, get some stats
        t = HumanHumanTournament("../annotate/emo20q.txt")
        assert isinstance(t,Tournament)
        assert type( t.matches() ) == list
        print(len(t.matches()))
        print([m.emotion() for m in t.matches()])
        #t.printStats()
        #engine = create_engine('sqlite:///emo20q.db', echo=True)
        #Base.metadata.create_all(engine)
        import networkx as nx
        from networkx import graphviz_layout
        import matplotlib.pyplot as plt

        G = nx.DiGraph()

        for m_idx,m in enumerate(t.matches()):
            assert isinstance(m,Match)
            assert type(m.turns()) == list
            G.add_nodes_from(m.turns())

            nx.draw(G)
            plt.show()
