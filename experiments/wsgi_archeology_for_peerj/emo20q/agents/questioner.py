#!/usr/bin/python

import Queue
import threading
import sys
import time
import os
import re
import nltk
import emo20q.nlp as nlp
from emo20q.models.episodicbuffer import EpisodicBuffer
from emo20q.models.semanticknowledge import SemanticKnowledge
from emo20q.models.lexicalaccess import LexicalAccess
from collections import defaultdict
from nltk.probability import DictionaryProbDist

#currently there is a problem, use the following input:
#ok, yes, maybe, no, depends, yes, no...

class QuestionerAgent(threading.Thread):
    """An agent that asks questions"""

    def __init__(self,dm):
        """create questioner agent"""
        threading.Thread.__init__(self)
        self.dialogManager = dm
        self.episodicBuffer = EpisodicBuffer()
        self.semanticKnowledge = SemanticKnowledge()
        self.lexicalAccess = LexicalAccess()
        # start with a uniform belief prior
        flat = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
        self.semanticKnowledge.setPriors(flat)
        self.state = None
        self.daemon = True  #important!
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
        #self._enterReplState = self.welcomeMessage
        self.welcomeMessage()
        #self._read = self.receivePatiently
        self._read = self.receive
        self._eval = lambda i: self.startIfReady(i)
        self._print = lambda i: self.send(i)
    def startIfReady(self,i):
        """checks if user is ready to start match"""
        if nlp.isReady(i):
            return self.toAskingState()
        else:
            return "let me know when you are ready"
    def toAskingState(self):
        """enter question asking state"""
        self.state = "asking"
        self._read = self.semanticYnReceivePatiently
        self._eval = self.evalAndAsk
        self._print = self.semanticSend
        self.send("Okay, let me see here...")
        return self.evalAndAsk()

    def toGuessingState(self,q):
        """enter guessing/confirmation state"""
        self.state = "guessing"
        self._read = self.semanticYnReceivePatiently
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
        if nlp.isReady(i):
            #reset prior
            flat = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
            self.semanticKnowledge.setPriors(flat)
            self.episodicBuffer.newMatch()
            return self.toAskingState()
        elif nlp.classifyYN(i) == -1:
            self.current_thread().exit()
            #sys.exit()
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
        if nlp.isAffirmative(i):
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
        probYes = defaultdict(float) 

        for ((label, fname), probdist) in self.semanticKnowledge._feature_probdist.items():
            #probNotNone[fname] += sumNotNone(probdist)*self.semanticKnowledge._label_probdist.prob(label)
            probYes[fname] += sumYes(probdist)*self.semanticKnowledge._label_probdist.prob(label)
        #we pick the question that is the maximum probability of being yes
        #among the questions not asked already
        result = max([x for x in probYes if x not in features],key=probYes.__getitem__)
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
        self.dialogManager.inputBuffer.put(("agent",msg))
    def semanticSend(self,gloss,delay=1):
        """
        sends a message, with optional delay
        Also, it addes information to the episodic buffer
        """
        msg = self.lexicalAccess.lookUp(gloss)
        time.sleep(delay)

        self.send("question %d: " % self.episodicBuffer.turnCount)

        self.episodicBuffer.addTurn("me",msg,self.state,gloss)
        self.dialogManager.inputBuffer.put(("agent",msg))
    def receive(self):
        """receives a message"""
        msg = self.dialogManager.toAgentBuffer.get()
        self.dialogManager.toAgentBuffer.task_done()
        self.episodicBuffer.addTurn("you",msg,self.state)
        return msg
    def receivePatiently(self):
        """receives a message while waiting for additional messages"""
        msg = self.dialogManager.toAgentBuffer.get()
        self.dialogManager.toAgentBuffer.task_done()
        while True:
            time.sleep(2)
            if self.dialogManager.toAgentBuffer.empty():
                break
            msg = msg + "\n" +  self.dialogManager.toAgentBuffer.get()
            self.dialogManager.toAgentBuffer.task_done()
        self.episodicBuffer.addTurn("you",msg,self.state)
        return msg
    def semanticYnReceivePatiently(self):
        """
        receives a YN message while waiting for additional messages
        Also, it addes information to the episodic buffer
        """
        msg = self.dialogManager.toAgentBuffer.get()
        self.dialogManager.toAgentBuffer.task_done()
        while True:
            time.sleep(2)
            if self.dialogManager.toAgentBuffer.empty():
                break
            msg = msg + "\n" +  self.dialogManager.toAgentBuffer.get()
            self.dialogManager.toAgentBuffer.task_done()

        sem = nlp.classifyYN(msg)
        self.episodicBuffer.addTurn("you",msg,self.state,semantics=sem)
        return msg

if __name__ == '__main__':
    print "shucks"
