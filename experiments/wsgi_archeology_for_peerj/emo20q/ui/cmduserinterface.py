#!/usr/bin/python
#import Queue
import threading
import sys
import time
#import os
#import re
#import emo20q.nlp as nlp
import signal

class CmdUserInterface(threading.Thread):
    def __init__(self,dm):
        self.dialogManager = dm
        threading.Thread.__init__(self)
        self.daemon = True  #important!
        self.startTime = time.time()
    def run(self):
        self.send("[User enters the Universe of Discourse]")
        while True:
            try:
                msg = self.receive()
                userInput = raw_input()
                self.send(userInput)
            except Exception as e:
                self.send(e)

    def send(self,msg):
        self.dialogManager.inputBuffer.put(("user",msg))
    def receive(self):
        #if not self.dialogManager.toUserBuffer.empty():
        if True:
            msg = self.dialogManager.toUserBuffer.get()
            self.dialogManager.toUserBuffer.task_done()
            return msg
        else:
            return None
            
