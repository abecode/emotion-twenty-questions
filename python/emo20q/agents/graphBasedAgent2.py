#!/usr/bin/python

# emo20q package imports
from emo20q.models.dialoggraph2  import DialogGraph
from emo20q.models.lexicalaccess import LexicalAccess

#external imports
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
    questions = sorted(s["Emotion"], key=ranking.get)
    #questions = sorted(s["Emotion"], key=G.out_degree)
    #questions = sorted(s["Emotion"], key=lambda x: nx.eccentricity(U,x))
    print questions
    Q.extend(questions)
    seen.extend(questions)
    history = []
    count = 0
    while(Q):
        count = count+1
        print "count ",count
        Q = sorted(Q, key=ranking.get)
        Q = deque(Q)
        print Q
        t = Q.pop()
        qgloss = t
        print "history"
        print history
        if history: 
            tmp1 = zip(*history)
            if qgloss in tmp1[0]: continue
        ans = ask(qgloss)
        history.append((qgloss,ans))
        if not G.neighbors(t): # we are dealing w/ guess as opposed to
                                    # question
            print "no neighbors"
            if ans == "yes": #found it
                print "awesome!"
                return t
            else:
                pass # no inference/action for wrong guess
        else:  # we were asking a question, as opp to guess
            try:
                print "try"
                successors = G.neighbors(qgloss)
                attributes = [G.get_edge_data(t,x).items()[0][1]['ans'] for x in successors]
                tmp =  zip(successors,attributes)
                successors,trash = zip(*filter(lambda x: x[1] == ans, tmp) )
                print "successors", successors
                #questions = sorted(s[t], key=ranking.get)
                #questions = sorted(s[t], key=lambda x: nx.eccentricity(U,x))
                #questions = sorted(successors, key=ranking.get)
                for q in questions:
                    if not q in seen:
                        seen.append(q)
                        if(ans == "yes"):
                            Q.append(q)
                        else:
                            Q.appendleft(q)
            except (KeyError,ValueError):
                print "KeyError/ValueError"
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
pr = nx.algorithms.link_analysis.pagerank_numpy(U)

search20q(D,pr)






