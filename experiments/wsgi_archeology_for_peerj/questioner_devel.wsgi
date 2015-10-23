#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import Cookie
import re
import sys
import os

info = """
<h1>  Emotion Twenty Questions (EMO20Q) Questioner Demo </h1>

<p>This is a game about emotions designed by researchers at USC's SAIL
lab. The goal is to provide a fun way to collect information about how people
understand and talk about their emotions. </p>


<p>To play, you will choose an emotion (not necessarily how you feel right
now--you can choose any emotion), then I (the EMO20Q computer algorithm) will
try to guess the emotion you've picked. </p>

<p> Please communicate with me as you would a real-life person, for example if we
were chatting online. Answer the questions to the best of your ability, and I
will use my emotional intelligence to try to guess the emotion you have
chosen. </p>

<p>If I guess an emotion that is an exact synonym of the emotion you picked, you
may accept it if you feel it is close enough (a good rule of thumb is that two
words are exact synonyms if you can't verbally express any difference between
the two words).</p>

<p>At the end of the match/game, I'll ask you for the correct emotion and you'll
have a chance to leave any private comments (public comments can be made using
the tab above).</p>

<p>Each match/game will take approximately 5 minutes and you are welcome to play as
many times as you like. For more information, check out the <a href="http://sail.usc.edu/emo20q"> Emotion Twenty Questions Homepage </a>. </p>

<form name="start"  method="get">
<input type="hidden" name="cmd" value="play">
<input type="submit" value="Start" />
</form>

"""

play = """
<html>
  <head>
    <script type="text/javascript">
      function setFocus()                                                          
      {                                                                            
        document.getElementById("response").focus();                            
      } 
    </script>
  </head>
  <body onload="setFocus()">
    <h1> Playing... </h1>
    %s
    <br/> %s <br/><br/><br/>
    <form name="play" method="get" >
      <input type="hidden" name="cmd" value="play"/>
      <input type="text" name="response" tabindex="1"  size="80" maxlength="200" id="response"/>
      <br/><br/><br/> (to submit, just hit return)
      <br/> (to quit, type ":quit" into the box and hit return)
    </form>
    
  </body>
<html>


"""


path = '/home/abe/emo20qgoogle/python'  # modify this for porting to other servers
if path not in sys.path:
    sys.path.insert(0,path)
sys.path.insert(0,path)


#from emo20q.agents.questioner import QuestionerAgent
import emo20q
from emo20q.agents.gpdaquestioner import QuestionerAgent,EpisodicBuffer
from emo20q.models.semanticknowledge import SemanticKnowledge
from emo20q.models.lexicalaccess import LexicalAccess

semanticKnowledge = SemanticKnowledge()
lexicalAccess = LexicalAccess()

import cPickle as pickle

def _play(environ, start_response):
    #import pickle
    #import cPickle as pickle

    global semanticKnowledge, lexicalAccess
    #check if there is a pickled agent using sessionid
    sessionid = environ['questioner.sessionid']
    pickledAgentPath = os.path.join(os.path.dirname(__file__),
                                "sessions/%s.agent"%sessionid)
    ##############################
    # restore from pickled state
    ##############################
    if os.path.exists(pickledAgentPath):
        try:
            episodicBuffer = pickle.load( open(pickledAgentPath,"rb") )
            agent = QuestionerAgent(episodicBuffer=episodicBuffer,
                                    lexicalAccess=lexicalAccess,
                                    semanticKnowledge=semanticKnowledge )
            
            agent.set_state(getattr(agent,agent.episodicBuffer.stateName))
            agent.belief = episodicBuffer.belief
        except (EOFError,AttributeError):
            print "reloading agent due to error"
            agent = QuestionerAgent()
    else:
        print "reloading agent due to no pickled file"
        agent = QuestionerAgent()

    parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
    if 'response' in parameters:
        response = cgi.escape(parameters['response'][0])
    else:
        response = ""
    
    #agentTurn = "<br/>".join([x for x in agent(response)])
    try:
        ######################
        # run agent
        ######################
        agentTurn = "<br/>".join(agent(response).split("\n"))
        info = "<h3> Question # %s</h3>"%str(agent.episodicBuffer.numTurns())
        output = play % (info,agentTurn)
        ##########################
        # repickle agent's state
        ##########################
        agent.episodicBuffer.stateName = agent.state.name
        agent.episodicBuffer.belief = agent.belief
        pickle.dump(agent.episodicBuffer,
                    open(pickledAgentPath,"wb"))
    
        #output += "response: %s"%response
        #output += "<h2>environ info</h2> <br/><br/> %s <br/><br/>"%(environ)
        status = '200 OK'
        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]

    except Exception, e:
        if re.search(r'endState',str(e)):
            return _quit(environ,start_response)
        else:
            print str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
            print(exc_type, fname, exc_tb.tb_lineno)
            raise e

def _quit(environ, start_response):
    status = '200 OK'
    output = "<h1>Quit</h1>"
    script = environ['PATH_INFO']+environ['SCRIPT_NAME']
    output += " <a href='%s'> If you'd like to play again, please click here</a>"%script
    #output += "<h2>environ info</h2> <br/><br/> %s <br/><br/>"%(environ)
    cookie = Cookie.SimpleCookie(environ.get('HTTP_COOKIE',''))
    cookie['sessionid'] = ""

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    response_headers += [("Set-Cookie", "%s=%s" % (x,cookie[x].value) ) for x in cookie.keys()]
    start_response(status, response_headers)
    return [output]

def dispatch(environ, start_response):
    lookup = { 'play': _play,
               'quit': _quit}
    try:
        return lookup[environ['questioner.cmd']](environ,start_response)
    except KeyError:
        output = "<h1> Oops! </h1>"
        output += "directive '%s' not found" % environ['questioner.cmd']
        status = '404 NOT FOUND!'
        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
        
    
def application(environ, start_response):
    if environ['PATH_INFO'] == "/favicon.ico":
        status = '400 Missing'
        output = " "
        response_headers = [('Content-type', 'text/raw'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]



    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)	  

    #tmp = "<h2>Hello Cruel World!</h2> <br/><br/> %s <br/><br/> %s "%(environ,form)

    # get cookie, set if not set
    cookie = Cookie.SimpleCookie(environ.get('HTTP_COOKIE',''))

    # Dispatch
    parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
    if 'cmd' in parameters and 'sessionid' in cookie and not cookie['sessionid'] == "":
        cmd = cgi.escape(parameters['cmd'][0])
        sessionid = cookie['sessionid'].value
        environ['questioner.cmd'] = cmd
        environ['questioner.sessionid'] = sessionid
        return dispatch(environ,start_response)
    else:
        print "create new session"
        output = info
        
        if 'sessionid' not in cookie or not cookie['sessionid'] == "":
            import uuid
            cookie['sessionid'] = uuid.uuid4()

        status = '200 OK'
        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(output)))]
        response_headers += [("Set-Cookie", "%s=%s" % (x,cookie[x].value) ) for x in cookie.keys()]
        start_response(status, response_headers)
        return [output]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    #server = make_server('localhost', 8081, application)
    server = make_server('0.0.0.0', 8081, application)  #this is public!
    #server = make_server('ark.usc.edu', 8081, application)
    server.serve_forever()
