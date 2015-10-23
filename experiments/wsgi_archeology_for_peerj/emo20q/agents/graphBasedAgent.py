#!/usr/bin/python

from emo20q.models.dialoggraph import DialogGraph
from emo20q.models.lexicalaccess import LexicalAccess

from collections import defaultdict
import re
import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from networkx.algorithms.traversal import *
import sys
from collections import deque

def search20q(G,ranking):
    seen = []
    seen.append("Emotion")
    Q = deque()
    s = bfs_successors(G,"Emotion")
    #aggregateRanking[q
    #questions = sorted(s["Emotion"], key=ranking.get)
    #questions = sorted(s["Emotion"], key=G.out_degree)
    questions = sorted(s["Emotion"], key=lambda x: nx.eccentricity(U,x))
    print questions
    Q.extend(questions)
    seen.extend(questions)
    history = []
    count = 0
    while(Q):
        count = count+1
        print count
        #Q = sorted(Q, key=ranking.get)
        #Q = deque(Q)
        print Q
        t = Q.pop()
        if isinstance(t,tuple): qgloss = t[0]
        else: qgloss = t
        print "history"
        print history
        if history: 
            tmp1 = zip(*history)
            if qgloss in tmp1[0]: continue
        ans = ask(qgloss)
        history.append((qgloss,ans))
        if not isinstance(t,tuple): # we are dealing w/ guess as opposed to
                                    # question
            if ans == "yes": #found it
                print "awesome!"
                return t
            else:
                pass # no inference/action for wrong guess
        elif isinstance(t,tuple):  # we were asking a question, as opp to guess
            try:
                successors = bfs_successors(G,(qgloss,ans))
                #questions = sorted(s[t], key=ranking.get)
                questions = sorted(s[t], key=lambda x: nx.eccentricity(U,x))
                for q in questions:
                    if not q in seen:
                        seen.append(q)
                        #if(ans == "yes"):
                        Q.append(q)
                        #else:
                        #    Q.appendleft(q)
            except KeyError:
                successors = []

            

def ask(qgloss):
    a = "other" 
    #q = L.lookUp(qgloss)
    q = qgloss
    userInput = raw_input(q+"\n? ")
    if userInput.find("yes") == 0 : a = "yes" 
    if userInput.find("no") == 0 : a = "no"
    return a

D = DialogGraph()
L = LexicalAccess()
T = bfs_tree(D,"Emotion")
s = bfs_successors(T,"Emotion")

U = D.to_undirected()
pr = nx.algorithms.link_analysis.pagerank(U)

search20q(D,pr)






