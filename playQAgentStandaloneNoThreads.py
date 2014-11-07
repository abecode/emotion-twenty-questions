#!/usr/bin/python

import sys
import time
import os
import re
import nltk
import logging
from collections import defaultdict
from nltk.probability import *
import uuid

from collections import defaultdict
from nltk.classify.naivebayes import NaiveBayesClassifier
import random

### BEGIN nlp #################################################################

def nlpIsReady(str):
    """
    check to see if the player is ready:
    Try to match affirmative answers to the question, are you ready? 
    """
    str = str.lower()
    match = re.search(r'\byes\b|\bready\b|\bsure\b|\bgo\b|\bok\b|\bokay\b', str)
    nomatch = re.search(r'\bno\b|\bnot\b', str)
    return match and not nomatch

def nlpClassifyYN(str):
    """"Classify answers to a yes/no question into 1/yes, -1/no, or 0/other"""
    str = str.lower()
    if re.search(r'\byes\b',str)  : ans = 1 
    elif re.search(r'\bno\b',str)  : ans = -1
    else: ans=0
    return ans
    
def nlpIsAffirmative(str):
    """"Classify answers to a yes/no question into 1/yes, -1/no, or 0/other"""
    if nlpClassifyYN(str) == 1:
        return True
    return False

### END nlp ###################################################################

### BEGIN base ################################################################

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
    def __init__(self, annotationFile="lists/onlineResults_2011-10-28.txt"):
        f = open(annotationFile, 'r')
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
            turns.append(turn)
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
        
    
class HumanHumanTournament(Tournament):
    """A set of emo20q matches played by two humans"""
    
    def __init__(self, annotationFile="annotate/emo20q.txt"):
#       self.base = Base()
		try:
			f = open(annotationFile, 'rU')
		except IOError as e:
			print e
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
        print "there are {0:d} matches".format(len(t.matches))
        #sum up the turns
        sumTurns = 0
        for m_idx,m in enumerate(t.matches):
            assert isinstance(m,Match)
            assert type(m._turns) == list
            print "  In match {0:d} there are {1:d} turns.".format(m_idx,len(m.turns))
            for tn_idx,tn in enumerate(m.turns()):
                assert isinstance(tn,Turn)
                #further tests
                sumTurns = sumTurns + len(m.turns())

        print "In all, there are {0:d} turns.".format(sumTurns)


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
                if re.match("end:",line):
                    fh.seek(-len(line),1)
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
    

### END base ##################################################################

### BEGIN LexicalAccess from lexicalaccess ####################################

class LexicalAccess():
   def __init__(self):
      # read in tournament, do some testing, get some stats
      tournament = HumanHumanTournament()
      
      self._dictionary = defaultdict(list)

      for m in tournament.matches():
         for t in m.turns():
            self._dictionary[t.questionId()].append(t.q)
   def lookUp(self,qgloss):
       candidates = self._dictionary[qgloss]
       if len(candidates) == 0:
          match = re.search(r'^e==(.+)$', qgloss)
          if match:  #deal with identity questions w/o lexical realizations
             return "is it %s?" % match.group(1)
          else:
             raise Exception("I didn't find a lexical realization for %s" % qgloss)
       return random.choice(candidates)
	   
### END LexicalAccess from lexicalaccess ######################################
	   
### BEGIN EpisodicBuffer from episodicbuffer ##################################

class EpisodicBuffer(list):
    """keep track of turns, using Episodic memory metaphor""" 
    def __init__(self):
        """create agent episodic memory buffer"""
        list.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__init__.__doc__)
        self.newMatch()
        self.turnCount = 1
    def addTurn(self,talker,utterance,state,semantics=None):
        turn = {}
        turn['talker'] = talker
        turn['utterance'] = utterance
        turn['state'] = state
        turn['ts'] = time.time()
        turn['mid'] = self.matchid
        turn['semantics'] = semantics
        if talker == "me" and semantics is not None:
            self.turnCount += 1
        self.append(turn)
        self.logger.info(turn)
    def newMatch(self):
        self.matchid = uuid.uuid4()
        self.logger.info("new match " + str(self.matchid))
        del self[:] #clear the episodic buffer
        self.turnCount = 1
		
### END EpisodicBuffer from episodicbuffer ####################################

### BEGIN SemanticKnowledge from semanticknowledge ############################

class SemanticKnowledge(NaiveBayesClassifier):
   
   def __init__(self):
      # read in tournament, do some testing, get some stats
      #tournament = HumanHumanTournament()
      tournament = (HumanHumanTournament()+HumanComputerTournament())
      
      #count turns in a dict, for pruning
      qcounts = defaultdict(int)
      for m in tournament.matches():
         for t in m.turns(): 
            qcounts[t.questionId()]+=1 
      
      feature_count_threshold  = 2
      # get list of emotions(entities/labels) and a list of
      # questions(properties/features)
      self._labels   = set()
      self._features = set()
      #get FreqDist of emotions(entities/labels)
      self._label_freqdist = FreqDist()
      #get FreqDist of questions(properties/features) given emotions
      self._feature_freqdist = defaultdict(FreqDist)
      self._feature_values = defaultdict(set)
      for m in tournament.matches():
         #print m.emotion()
         emotions = m.emotion().split("/") #deal with synonyms (sep'd w/ '/' )
         for e in emotions:
            self._labels.add(e)
            self._label_freqdist.inc(e) 
            for t in m.turns():
               qid = t.questionId()
               if(qcounts[qid] >= feature_count_threshold):
                  #deal with b.s. questions
                  if (qid.find("non-yes-no")==0): continue
                  if (qid.find("giveup")==0): continue
                  self._features.add(qid)
                  #convert answer to yes/no/other
                  ans = t.answerId()
                  #if ans == "other": continue         
                  #deal with guesses:
                  #guess = re.search(r'^e==(\w+)$',t.qgloss )
                  #if(guess):
                  self._feature_freqdist[e,qid].inc(ans)
                  self._feature_values[qid].add(ans)

      # assign "None" to properties of entities when property is unseen
      for e in self._labels: 
         num_samples = self._label_freqdist[e] 
         for fname in self._features: 
            count = self._feature_freqdist[e, fname].N() 
            if count == 0:
               self._feature_freqdist[e, fname].inc(None) 
               self._feature_values[fname].add(None) 
               #these next 3 lines are questionable
               self._feature_values[fname].add("yes") 
               self._feature_values[fname].add("no") 
               self._feature_values[fname].add("other") 

      # Create the P(label) distribution 
      self._label_probdist =  ELEProbDist(self._label_freqdist) 


      # Create the P(fval|label, fname) distribution 
      self._feature_probdist = {} 
      for ((label, fname), freqdist) in self._feature_freqdist.items(): 
         probdist = ELEProbDist(freqdist, bins=len(self._feature_values[fname])) 
         self._feature_probdist[label,fname] = probdist 

   def entities(self):
      return self._labels
   def properties(self):
      return self._features
   def prior(self):
      return self._label_probdist
   def likelihood(self,observation,model):
      pass
   def setPriors(self,label_probdist):
      if not isinstance(label_probdist,ProbDistI):
         try:
            label_probdist = ELEProbDist(label_probdist)
         except:
            pass

      self._label_probdist = label_probdist
   

   def show_most_informative_features(self, n=20): 
      # Determine the most relevant features, and display them. 
      cpdist = self._feature_probdist 
      print 'Most Informative Features' 
   
      for (fname, fval) in self.most_informative_features(n): 
         def labelprob(l): 
            return cpdist[l,fname].prob(fval)       
         labels = sorted([l for l in self._labels 
                          if fval in cpdist[l,fname].samples()], 
                         key=labelprob) 
         if len(labels) == 1: continue 
         l0 = labels[0] 
         l1 = labels[-1] 
         if cpdist[l0,fname].prob(fval) == 0: 
            ratio = 'INF' 
         else: 
            ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) / 
                               cpdist[l0,fname].prob(fval)) 
         print ('%24s = %-14r %6s : %-6s = %s : 1.0' % 
                (fname, fval, str(l1)[:6], str(l0)[:6], ratio)) 

   def most_informative_features(self, n=20): 
      """ 
      Return a list of the 'most informative' features used by this 
      classifier.  For the purpose of this function, the 
      informativeness of a feature C{(fname,fval)} is equal to the 
      highest value of P(fname=fval|label), for any label, divided by 
      the lowest value of P(fname=fval|label), for any label:: 
      
            max[ P(fname=fval|label1) / P(fname=fval|label2) ] 
            """ 
          # The set of (fname, fval) pairs used by this classifier. 
      features = set() 
      # The max & min probability associated w/ each (fname, fval) 
      # pair.  Maps (fname,fval) -> float. 
      maxprob = defaultdict(lambda: 0.0) 
      minprob = defaultdict(lambda: 1.0) 
      
      for (label, fname), probdist in self._feature_probdist.items(): 
         for fval in probdist.samples(): 
            feature = (fname, fval) 
            features.add( feature ) 
            p = probdist.prob(fval) 
            #print label,feature,p
            maxprob[feature] = max(p, maxprob[feature]) 
            minprob[feature] = min(p, minprob[feature]) 
            if minprob[feature] == 0: 
               features.discard(feature) 
   
      # Convert features to a list, & sort it by how informative 
      # features are. 
      features = sorted(features,  
                        key=lambda feature: minprob[feature]/maxprob[feature]) 
      return features[:n] 

### END SemanticKnowledge from semanticknowledge ##############################
	  
### BEGIN QuestionerAgent from questioner #####################################

logging.basicConfig(filename='questioner.log',level=logging.DEBUG)
logging.info('starting logger in questioner.py')
				
#class QuestionerAgent(threading.Thread):
class QuestionerAgent():
    """An agent that asks questions"""

    def __init__(self):
        """create questioner agent"""
        #threading.Thread.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(self.__init__.__doc__)
        #self.dialogManager = dm
        self.episodicBuffer = EpisodicBuffer()
        self.semanticKnowledge = SemanticKnowledge()
        self.lexicalAccess = LexicalAccess()
        # start with a uniform belief prior
        flat = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
        self.semanticKnowledge.setPriors(flat)
        self.state = None
        #self.daemon = True  #important!
    def runNoThread(self):
        """thread main loop"""
        print "[Agent enters the Universe of Discourse]"
        self.toInitialState()
        self.repl()
    def run(self):
        """thread main loop"""
        self.send("[Agent enters the Universe of Discourse]")
        self.toInitialState()
        try:
            while True:
                self.repl()
        except Exception as e:
           self.send(e) 
            
    def repl(self):
        """
        read-evaluate-print loop.  
        note: _read, _eval, and _print are monkey patched
        """
        #self._enterReplState()
        while True:
            #self._print(self._eval(self._read()))
            tmp = self._read()
            #print tmp
            tmp = self._eval(tmp)
            self._print(tmp)
            tmp = None
    def welcomeMessage(self):
        """prints welcome message"""
        self.send("Welcome to Emo20Q")
        self.send("I'm going to try to guess the emotion you are thinking of")
        self.send("it needn't be the emotion you are currently feeling")
        self.send("Let me know when you are ready")
    def toInitialState(self):
        """enter initial state"""
        self.state = "initial"
        self.welcomeMessage()
        self._read = self.receive
        self._eval = lambda i: self.startIfReady(i)
        self._print = lambda i: self.send(i)
    def startIfReady(self,i):
        """checks if user is ready to start match"""
        if nlpIsReady(i):
            return self.toAskingState()
        else:
            return "let me know when you are ready"
    def toAskingState(self):
        """enter question asking state"""
        self.state = "asking"
        self._read = self.semanticYnReceive
        self._eval = self.evalAndAsk
        self._print = self.semanticSend
        self.send("Okay, let me see here...")
        return self.evalAndAsk()

    def toGuessingState(self,q):
        """enter guessing/confirmation state"""
        self.state = "guessing"
        self._read = self.semanticYnReceive
        self._eval = self.confirmGuess
        self._print = self.semanticSend
        return q

    def toBetweenMatchesState(self):
        """enter guessing/confirmation state"""
        self.state = "betweenMatches"
        self._read = self.receive
        self._eval = lambda i: self.continueOrQuit(i)
        self._print = lambda i: self.send(i)
        return  "Would you like to play again?"
    def continueOrQuit(self,i):
        """checks if user is ready to start match"""
        if nlpIsReady(i):
            #reset prior
            flat = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
            self.semanticKnowledge.setPriors(flat)
            self.episodicBuffer.newMatch()
            return self.toAskingState()
        elif nlpClassifyYN(i) == -1:
            print "Okie dokie, bye then..."
            sys.exit()
        else:
            return "let me know when you are ready"


    def evalAndAsk(self,*args):

        if self.episodicBuffer.turnCount > 20:
            self.send("Dammit, I failed. ")
            return self.toBetweenMatchesState()

        #if args:
            #self.send("you said %s " % str(args[0]))
        # check for semantically relevant and mnemonically accessible items in
        # the episodic buffer
        agentTurns = filter(lambda i: i['semantics'] is not None and i['talker'] == "me", 
                               self.episodicBuffer)
        userTurns = filter(lambda i: i['semantics'] is not None and i['talker'] == "you", 
                               self.episodicBuffer)
        #list features
        features = {}
        #self.send("my episodic buffer has %d units of information" % 
        #          len(userTurns))
        for (a,u) in zip(agentTurns,userTurns):
            #self.send("I asked '%s'" % a['utterance'])
            #self.send("...and you said '%s'" % u['utterance'])
            f = self.getFeature(a,u)
            #self.send("which I interpreted as '%s'" % str(f))
            for k,v in f.items():
                features[k] = v

        if len(features) == 0:
        #if True:
            #return self.pickNextQuestion(self,features)
            return "e.valence==positive"
            #return "e==happiness"
    
        else:
            #update probabilities
            try:
                #post = self.semanticKnowledge.prob_classify({"e.valence==postive":"yes"})
                post = self.semanticKnowledge.prob_classify(f)
                #self.send("Based on this data, I think you may have picked one of the following")
                #out = ", ".join(sorted(post.samples(),key=post.prob,reverse=True)[0:10])
                #self.send(out)
                self.semanticKnowledge.setPriors(post)
                #self.send("But I will continue to ask...")
                #self.sendHesitation
                
                nextQuestion = self.pickNextQuestion(features)
                # switch to guessing emotion identity if the next 
                # question is an identity question,
                if(re.search(r"^e==",nextQuestion)):
                    return self.toGuessingState(nextQuestion)

                return nextQuestion
            except Exception as e:
                self.send(e)

    def confirmGuess(self,i):
        """checks if the guess is correct to start match"""
        if nlpIsAffirmative(i):
            self.send("yeah! Thanks for playing",1.5)
            return self.toBetweenMatchesState()
        else:
            #self.send("okay, I'll continue, but just let me update by belief vector")
            agentTurns = filter(lambda i: i['semantics'] is not None and i['talker'] == "me", 
                               self.episodicBuffer)
            tmpGloss = agentTurns[-1]['semantics']
            match = re.search(r'^e==(.+)$', tmpGloss)
            if(match):
                tmpEmo = match.group(1)
                tmpDict = dict((key, self.semanticKnowledge._label_probdist.prob(key)) for key in self.semanticKnowledge._label_probdist.samples())
                tmpDict[tmpEmo] = 0
                self.semanticKnowledge._label_probdist = DictionaryProbDist(tmpDict,normalize=True)
                #assert(self.semanticKnowledge._label_probdist.prob(tmpEmo)==0)
                return self.toAskingState()
            else: #there was some kind of error
                self.send("oops, I misinterpreted some stuff and must quit")
                self.send(Exception())


    def getFeature(self,agentTurn,userTurn):
        if("semantics" not in agentTurn or "semantics" not in userTurn): 
            raise Exception("no freaking semantics")
        answer = None
        if userTurn['semantics'] == 1  : answer = "yes"
        if userTurn['semantics'] == 0  : answer = "other"
        if userTurn['semantics'] == -1 : answer = "no"
        return {agentTurn['semantics']:answer}

    def pickNextQuestion(self,features):
        #sort the question/features by probability of being != None
        #self.send("starting to pick next question based on the following features in my episodic buffer: %s" % str(features))
        def sumNotNone(probdist):
            return sum([probdist.prob(x) for x in ("yes","no","other")])
        def sumYes(probdist):
            return probdist.prob("yes")
        probNotNone = defaultdict(float) 
        for ((label, fname), probdist) in self.semanticKnowledge._feature_probdist.items():
            #probNotNone[fname] += sumNotNone(probdist)*self.semanticKnowledge._label_probdist.prob(label)
            probNotNone[fname] += sumYes(probdist)*self.semanticKnowledge._label_probdist.prob(label)
        result = max([x for x in probNotNone if x not in features],key=probNotNone.__getitem__)
        match = re.search(r'^e==(.+)$', result)
        # if identity question or turnCount==20, choose from belief vector
        if  match or self.episodicBuffer.turnCount>=20:
            guess = sorted(self.semanticKnowledge._label_probdist.samples(),key=self.semanticKnowledge._label_probdist.prob,reverse=True)[0]
            return "e==%s" % guess
        else:
            return result
    def send(self,msg,delay=0.5):
        """sends a message, with optional delay"""
        time.sleep(delay)
        self.episodicBuffer.addTurn("me",msg,self.state)
        #self.dialogManager.inputBuffer.put(("agent",msg))
        print msg
    def semanticSend(self,gloss,delay=1):
        """
        sends a message, with optional delay
        Also, it addes information to the episodic buffer
        """
        msg = self.lexicalAccess.lookUp(gloss)
        time.sleep(delay)

        self.send("question %d: " % self.episodicBuffer.turnCount)

        self.episodicBuffer.addTurn("me",msg,self.state,gloss)
        print msg
    def receive(self):
        """receives a message"""
        msg = raw_input("input> ")
        self.episodicBuffer.addTurn("you",msg,self.state)
        return msg

    def semanticYnReceive(self):
        """
        receives a YN message while waiting for additional messages
        Also, it addes information to the episodic buffer
        """
        msg = raw_input("input> ")
        sem = nlpClassifyYN(msg)
        self.episodicBuffer.addTurn("you",msg,self.state,semantics=sem)
        return msg

if __name__ == '__main__':
    a = QuestionerAgent()
    a.runNoThread()

