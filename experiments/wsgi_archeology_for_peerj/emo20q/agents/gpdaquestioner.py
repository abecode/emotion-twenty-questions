#!/usr/bin/python

"""
A questioner agent based on the notion of a generalized pushdown automaton,
which is just a pushdown automaton that can look at his/her whole stack

"""
import emo20q
import emo20q.nlp
from emo20q.models.generalizedpushdownautomaton import GPDA,State,GPDAError
from emo20q.models.semanticknowledge import SemanticKnowledge
from emo20q.models.lexicalaccess import LexicalAccess
import nltk
from collections import defaultdict
import re
import random

class EpisodicBuffer(list):
    def __init__(self):
        super(list,self).__init__()
    def add(self,input,semantics=None):
        input.semantics = semantics
        if isinstance(input,Question):
            input.talker = "agent"
            self.append(input)
        elif isinstance(input,Answer):
            input.talker = "user"
            q = self.pop()
            if isinstance(q,Question):
                t = Turn(q,input)
                self.append(t)
            elif isinstance(q,AgentUtt):
                self.append(q)
                self.append(input)
            else:
                raise GPDAError("Stack content error")
        elif isinstance(input,AgentUtt):
            input.talker = "agent"
            self.append(input)
        elif isinstance(input,UserUtt):
            input.talker = "user"
            self.append(input)
        else:
            raise GPDAError("Stack content error")
    def newMatch(self):
        del self[:]
    def numTurns(self):
        turns = filter(lambda x: isinstance(x,Turn) or isinstance(x,Question),self)
        return len(turns)
    def getFeature(self,q,a):
        if(not q.gloss): 
            raise Exception("no gloss")
        answer = None
        if emo20q.nlp.classifyYN(a.text) == 1 : answer = "yes"
        elif emo20q.nlp.classifyYN(a.text) == -1  : answer = "no"
        else : answer = "other"
        return (q.gloss,answer)


    def getFeatures(self):
        turns = filter(lambda x: isinstance(x,Turn),self)
        features = {}
        for x in turns:
            f = self.getFeature(x.q,x.a)
            features[f[0]]=f[1]
        return features


        
class QuestionerAgent(GPDA):
    """
    this class is a rewrite/refactor of the older agent as a generalized pushdown automaton
    
    it is hoped that this will make the design more principled

    >>> agent = GPDAQuestioner()

    # start in startState
    >>> agent.state.name
    'startState'
    
    # fire up this ol' automaton
    >>> print agent("")
    [Agent enters the universe of discourse]
    Welcome to EMO20Q
    I'm goint to try to guess the emotion that you are thinking of
    it needn't be the emotion you are currently feeling
    Let me know when you are ready...

    # test him out
    >>> agent("fasdfadsf")
    'Let me know when you are ready... (some people get stuck here... try typing something into the box to let me know whether you are ready, or not)'
    
    >>> print agent("ok fine") #doctest: +ELLIPSIS
    Ok, let me see here...
    ...
    
    
    """

    startState = State("startState")
    welcomeState = State("welcomeState")
    askingState = State("askingState")
    confirmingState = State("confirmingState")
    reviewingState = State("reviewingState")
    betweenMatchesState = State("betweenMatchesState")
    endState = State("endState")
    
    
    
    def __init__(self, 
                 episodicBuffer=EpisodicBuffer(),
                 semanticKnowledge=SemanticKnowledge(),
                 lexicalAccess=LexicalAccess() ):
        super(QuestionerAgent,self).__init__()
        self.episodicBuffer = episodicBuffer
        self.semanticKnowledge = semanticKnowledge
        self.lexicalAccess = lexicalAccess
        self.stack = self.episodicBuffer
        

        self.belief =  nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
        # to welcome message from startState
        self.add_transition(self.startState,self.welcomeState,
                            test=lambda x: True, #transition on any input
                            function=self.welcomeMessage)
        # reprompt til ready (loop in welcomeState)
        self.add_transition(self.welcomeState,self.welcomeState,
                            test=lambda x: not emo20q.nlp.isReady(x), 
                            function=lambda x: "Let me know when you are ready... (some people get stuck here... try typing something into the box to let me know whether you are ready, or not)",
                            )
        #start match, to asking state from welcomeState
        self.add_transition(self.welcomeState,self.askingState,
                            test=emo20q.nlp.isReady, 
                            function=self.beginPlaying)
        #main asking loop
        self.add_transition(self.askingState,self.askingState,
                            test=self.shouldIAsk, 
                            function=self.evaluateQuestionAnswer)
        self.add_transition(self.askingState,self.confirmingState,
                            test=lambda x: emo20q.nlp.isAffirmative(x) and self.episodicBuffer[-1].isIdentityQuestion(), 
                            function=self.confirmAnswer)
        #sucess! to betweenMatchesState from confirmingState
        self.add_transition(self.confirmingState,self.betweenMatchesState,
                            test=emo20q.nlp.isAffirmative, 
                            function=self.doYouWantToPlayAgainSuccess)
        #a failed guess w/ <20 questions, to askingState from confirmingState
        self.add_transition(self.confirmingState,self.askingState,
                            test=lambda x: not emo20q.nlp.isAffirmative(x) and self.shouldIAsk(x), 
                            function=self.evaluateQuestionAnswer)
        #a failed guess, >20 questions, to reviewingState
        self.add_transition(self.confirmingState,self.reviewingState,
                            test=lambda x: not emo20q.nlp.isAffirmative(x) and self.episodicBuffer.numTurns()>=20, 
                            function=self.reviewAnswerAfterDisconfirm)
        #ran out of questions, ask what the emotion was, to reviewingState
        self.add_transition(self.askingState,self.reviewingState,
                            test=self.shouldIReview, 
                            function=self.reviewAnswer)
        #failed match, but try again, to betweenMatchesState from reviewingState
        self.add_transition(self.reviewingState,self.betweenMatchesState,
                            test=lambda x: True, 
                            function=self.doYouWantToPlayAgain)
        #replay 
        self.add_transition(self.betweenMatchesState,self.welcomeState,
                            test=emo20q.nlp.isAffirmative, 
                            function=self.replayMessage)
        #no replay 
        self.add_transition(self.betweenMatchesState,self.endState,
                            test=lambda x: not emo20q.nlp.isAffirmative(x), 
                            function=self.goodbyeMessage)


        self.state = self.startState
    def processGlobalCommands(self,input):
        if re.match(r':quit',input):
            raise GPDAError("endState via :quit")
    def welcomeMessage(self,input):
        output = "[Agent enters the universe of discourse]\n"
        output += "Welcome to EMO20Q\n"
        output += "I'm goint to try to guess the emotion that you are thinking of\n"
        output += "it needn't be the emotion you are currently feeling\n"
        output += "Let me know when you are ready..."
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def replayMessage(self,input):
        self.episodicBuffer.newMatch()
        self.episodicBuffer.add(UserUtt(input))
        output = "Cool.  Let me know when you think of another emotion... "
        output += "Let me know when you are ready...\n"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def goodbyeMessage(self,input):
        self.episodicBuffer.add(UserUtt(input))
        output = "Thank you for playing"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def beginPlaying(self,input):
        self.episodicBuffer.add(UserUtt(input))
        output = "Ok, let me see here... \n"
        nextQ = self.pickNextQuestion()        
        output += self.lexicalAccess.lookUp(nextQ)
        self.episodicBuffer.add(Question(output,gloss=nextQ))
        return output
    def evaluateQuestionAnswer(self,input):
        self.episodicBuffer.add(Answer(input))
        if self.episodicBuffer.numTurns() >= 20:
            raise GPDAError("shouldn't be asking with 20 or more questions")
        #output = "ok, I see.  Number %s. Is it a bla bla bla?"%str(self.episodicBuffer.numTurns()+1)
        ##############################
        #update belief: key part!
        ##############################
        features = self.episodicBuffer.getFeatures()
        self.semanticKnowledge.setPriors(self.belief)
        post = self.semanticKnowledge.prob_classify(features)
        # if last question was an identity question (guess), then zero out that emotion
        if hasattr(self.episodicBuffer[-1].q, "isIdentityQuestion") and self.episodicBuffer[-1].q.isIdentityQuestion():
            match = re.search(r'^e==(.+)$', self.episodicBuffer[-1].q.gloss)
            tmpDict = dict((key, post.prob(key)) for key in post.samples())
            #tmpDict[tmpEmo] = 0
            #self.semanticKnowledge._label_probdist = DictionaryProbDist(tmpDict,normalize=True)
            tmpDict[match.group(1)] = 0
            #print sorted([key for key in tmpDict], key=tmpDict.__getitem__,reverse=True)
            post = nltk.probability.DictionaryProbDist(tmpDict,normalize=True)
        self.belief = post
        print Belief(self.belief)
        #self.episodicBuffer.add(Belief(self.belief))
        nextQ = self.pickNextQuestion()
        output = self.lexicalAccess.lookUp(nextQ)
        self.episodicBuffer.add(Question(output,gloss=nextQ))
        #for x in self.stack:
        #    print x
        return output
    def shouldIAsk(self,input):
        print self.episodicBuffer.numTurns()
        if hasattr(self.episodicBuffer[-1],'isIdentityQuestion') and self.episodicBuffer[-1].isIdentityQuestion() and emo20q.nlp.isAffirmative(input):
            return False
        if self.episodicBuffer.numTurns() < 20:
            return True
        return False
    def shouldIReview(self,input):
        if self.episodicBuffer.numTurns() >= 20 and not (self.episodicBuffer[-1].isIdentityQuestion() and  emo20q.nlp.isAffirmative(input)):
            return True
        return False
    def confirmAnswer(self,input):
        self.episodicBuffer.add(Answer(input))
        output = "so did I get it right?"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def reviewAnswer(self,input):
        self.episodicBuffer.add(Answer(input))
        output = "Dammit, that is disappointing... \n"
        output += "Well, what was the emotion that you picked?"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def reviewAnswerAfterDisconfirm(self,input):
        self.episodicBuffer.add(UserUtt(input))
        output = "Dammit, that is disappointing... \n"
        output += "Well, what was the emotion that you picked?"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def doYouWantToPlayAgainSuccess(self,input):
        self.episodicBuffer.add(UserUtt(input))
        #self.episodicBuffer.save()
        self.belief = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
        self.episodicBuffer.newMatch()
        output = "Awesome!\n"
        output += "Would you like to play again?"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    def doYouWantToPlayAgain(self,input):
        self.episodicBuffer.add(UserUtt(input))
        #self.episodicBuffer.save()
        self.belief = nltk.probability.UniformProbDist(self.semanticKnowledge.entities())
        self.episodicBuffer.newMatch()
        output = "Would you like to play again?"
        self.episodicBuffer.add(AgentUtt(output))
        return output
    
    def pickNextQuestion(self):
        #sort the question/features by probability of being != None
        #self.send("starting to pick next question based on the following features in my episodic buffer: %s" % str(features))
        features = self.episodicBuffer.getFeatures()
        def sumNotNone(probdist):
            return sum([probdist.prob(x) for x in ("yes","no","other")])
        def sumYes(probdist):
            return probdist.prob("yes")
        probYes = defaultdict(float) 

        for ((label, fname), probdist) in self.semanticKnowledge._feature_probdist.items():
            #probNotNone[fname] += sumNotNone(probdist)*self.semanticKnowledge._label_probdist.prob(label)
            #probYes[fname] += sumYes(probdist)*self.semanticKnowledge._label_probdist.prob(label)
            probYes[fname] += sumYes(probdist)*self.belief.prob(label)
        #we pick the question that is the maximum probability of being yes
        #among the questions not asked already
        result = max([x for x in probYes if x not in features],key=probYes.__getitem__)
        match = re.search(r'^e==(.+)$', result)
        # if identity question or turnCount==20, choose from belief vector
        if  match or self.episodicBuffer.numTurns()>=18:  #choose an ID question (guess)
            guess = sorted(self.semanticKnowledge._label_probdist.samples(),key=self.belief.prob,reverse=True)[0]
            return "e==%s" % guess
        else:
            return result
    def printTopQuestions(self,n=10,wrs=False):
        #sort the question/features by probability of being != None
        #self.send("starting to pick next question based on the following features in my episodic buffer: %s" % str(features))
        features = self.episodicBuffer.getFeatures()
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
        if wrs:
            result = sorted([x for x in probYes if x not in features],key=lambda x:probYes[x]*random.random(), reverse=True)
        else:
            result = sorted([x for x in probYes if x not in features],key=probYes.__getitem__, reverse=True)
        return result[0:n]
        


class Utterance(object):
    def __init__(self,text,gloss=None):
        self.text = text
        self.gloss = gloss
class AgentUtt(Utterance):
    pass
class UserUtt(Utterance):
    pass
class Question(AgentUtt):
    def isIdentityQuestion(self):
        if re.search(r'^e==(.+)$', self.gloss):
            return True
        else:
            return False
        

class Answer(UserUtt):
    pass
    
class Turn(object):
    def __init__(self,q,a):
        self.q = q
        self.a = a

class Belief(dict):
    def __init__(self,probdist):
        """Takes an nltk probdist and returns a dict/multinomial distribution"""
        for key in probdist.samples():
            self[key] = probdist.prob(key)
    def __repr__(self):
        output = "Belief({\n"
        for x in sorted([key for key in self],key=self.__getitem__):
            output += "'%s':'%s'\n"%(x,self[x])
        output += "})"
        return output
            
            
if __name__ == "__main__":
    import argparse
    argParser = argparse.ArgumentParser(description="""A generalized pushdown automaton implementation of an EMO20Q questioner agent.  """)
    argParser.add_argument('-t', '--test', 
                           action='store_true',
                           help='test using doctest')
    argParser.add_argument('--run', 
                           action='store_true',
                           help='run the agent interactively on the commandline')
    args = argParser.parse_args()
    if args.test: 
        import doctest
        doctest.testmod()
    elif args.run:
        input = ""
        agent = QuestionerAgent()
        while True:
            print agent(input)
            input = raw_input("> ") 
            
