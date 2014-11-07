#!/usr/bin/python
import Queue
import threading
import sys
import time
import os
import re
import emo20q.nlp as nlp
import signal

class DialogManager(threading.Thread):
    playersAreOkay = True
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.inputBuffer = Queue.Queue()
        self.toUserBuffer = Queue.Queue()
        self.toAgentBuffer = Queue.Queue()
        self.history = []
    #     signal.signal(signal.SIGINT, self.terminate)
    # def terminate(self,signal,frame):
    #     playersAreOkay = False
    #     return 0
    def run(self):
        print "Starting Dialog Manager"
        #while True:
        while self.playersAreOkay:
            try:
            #if(a.is_alive() and u.is_alive()):
                if(True):
                    (sender,msg) = self.inputBuffer.get()
                    #if msg == "": break
                    self.inputBuffer.task_done()
                    os.system("clear")
                    self.history.append((sender,msg))
                    for h in self.history:
                        print h
                    if re.search(r'^\[.+\]$',msg):
                        continue   #status message
                    if sender == "agent":
                        self.toUserBuffer.put(msg)
                    if sender == "user":
                        self.toAgentBuffer.put(msg)
                    #dm.inputBuffer.task_done()
                    # if(not a.is_alive()):
                    #     print "agent is dead"
                    #     raise Exception("DeadPlayer")
                    # elif(not u.is_alive()):
                    #     print "agent is dead"
                    #     raise Exception("DeadPlayer")
                        
                        # else:
                        #     pass
            except Exception as e:
                print "caught",e,"in dialogmanager.py"
                print sys.exc_info()[0]
                sys.exit()
                        
class MockAgent(threading.Thread):
    def __init__(self,dm):
        self.dialogManager = dm
        #signal.signal(signal.SIGINT, self.dialogManager.terminate)
        threading.Thread.__init__(self)
        self.daemon = True  #important!

    def run(self):
        self.send("[Agent enters the Universe of Discourse]")
        self.toInitialState()
        try:
            while True:
                self.repl()
        except:
            print "oh crap"

    def toInitialState(self):
        #self._enterReplState = self.welcomeMessage
        self.welcomeMessage()
        #self._read = self.receivePatiently
        self._read = self.receive
        self._eval = lambda i: self.readyToStart(i)
        self._print = lambda i: self.send(i)

    def toBrainlessState(self):
        self._read = self.receive
        self._eval = lambda i: "you said %s" % i
        self._print = lambda i: self.send(i)
        #self.send("Sorry, I appear to be missing my brain")
        return "Sorry, I appear to be missing my brain"
        
    def repl(self):
        #self._enterReplState()
        while True:
            msg = self._read()
            conclusion = self._eval(msg)
            #print conclusion
            if(conclusion):
                self._print(conclusion)
                conclusion = None
            
    def welcomeMessage(self):
        self.send("Welcome to Emo20Q",0)
        self.send("I'm going to try to guess the emotion you are thinking of",0)
        self.send("it needn't be the emotion you are currently feeling",0)
        self.send("Let me know when you are ready",0)
        #msg = self.receive()
        #if msg == "yes":
        #    self.repl = self.repl_brainless
    def readyToStart(self,msg):
        if nlp.isReady(msg):
            return self.toBrainlessState()
        else:
            return "let me know when you are ready...."
            

    def send(self,msg,delay=1):
        time.sleep(delay)
        self.dialogManager.inputBuffer.put(("agent",msg))
    def receive(self):
        msg = self.dialogManager.toAgentBuffer.get()
        self.dialogManager.toAgentBuffer.task_done()
        return msg
    def receivePatiently(self):
        msg = self.dialogManager.toAgentBuffer.get()
        self.dialogManager.toAgentBuffer.task_done()
        while True:
            time.sleep(5)
            if self.dialogManager.toAgentBuffer.empty():
                break
            msg = msg + "\n" +  self.dialogManager.toAgentBuffer.get()
            self.dialogManager.toAgentBuffer.task_done()
        return msg

class MockUser(threading.Thread):
    def __init__(self,dm):
        self.dialogManager = dm
        threading.Thread.__init__(self)
        self.daemon = True  #important!
        self.startTime = time.time()
    def run(self):
        while True:
            msg = self.receive()
            time.sleep(1)
            if(time.time()-self.startTime <15): # silliness for 15 sec
                self.send("omg, it works.  it just said \"%s\"" % msg)
            else:
                self.send("omg, this is silly, I'm going home")
                return

    def send(self,msg):
        self.dialogManager.inputBuffer.put(("user",msg))
    def receive(self):
        msg = self.dialogManager.toUserBuffer.get()
        self.dialogManager.toUserBuffer.task_done()
        return msg


class SimpleUserInterface(threading.Thread):
    def __init__(self,dm):
        self.dialogManager = dm
        threading.Thread.__init__(self)
        self.daemon = True  #important!
        self.startTime = time.time()
        #signal.signal(signal.SIGINT, self.dialogManager.terminate)
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
            
if __name__ == '__main__':
    
    from emo20q.controllers.dialogmanager import DialogManager
    from emo20q.controllers.dialogmanager import MockAgent
    from emo20q.controllers.dialogmanager import SimpleUserInterface
    import signal

    global goodToGo
    goodToGo=True
    def tmp(sig,frame):
        global goodToGo
        goodToGo = False
        print (sig,frame)
        raise Exception(sig,frame)
    signal.signal(signal.SIGINT, lambda sig,frame:  tmp(sig,frame))

    dm = DialogManager()
    a = MockAgent(dm)
    #u = MockUser(dm)
    u = SimpleUserInterface(dm)
    try:
        dm.start()
        a.start()
        u.start()
        #dm.start()

    #except None:#(KeyboardInterrupt, SystemExit, Exception):
    except (KeyboardInterrupt,EOFError, SystemExit, Exception):
        sys.exit()

