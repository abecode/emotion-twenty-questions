#!/usr/bin/python
import uuid
import logging
import time

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
