#!/usr/bin/python

from emo20q.data.base import HumanHumanTournament
import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import sys
from collections import defaultdict

try: sys.argv[1]
except:   
   print "no argument given"
   sys.exit(1)

# read in tournament, do some testing, get some stats
tournament = HumanHumanTournament("../annotate/emo20q.txt")

#count turns in a dict, for pruning
qcounts = defaultdict(int)
for m in tournament.matches():
   for t in m.turns(): 
       qcounts[t.qgloss]+=1 

#create graph
G = nx.DiGraph()
G.add_node(("Emotion",))

#add emo20q data to graph
for m_idx,m in enumerate(tournament.matches()):
   H = nx.DiGraph()
   parent = ("Emotion"),
   #parent = ()
   H.add_node(parent)
   for t in m.turns():
      if(qcounts[t.qgloss]>0):
         #deal with guesses:
         guess = re.search(r'^e==(\w+)$',t.qgloss )
         if(guess):
            #H.add_edge(parent,guess.group(1))
            H.add_edge(parent,guess.group(1),weight=20)
            #G.add_nodes_from(H)
            continue
         #deal with questions
         if (t.qgloss == "non-yes-no"): continue
         if (t.qgloss == "giveup"): continue
         ans = "other" 
         if t.agloss.find("yes") == 0 : 
            ans = "yes" 
            weight = 1
         if t.agloss.find("no") == 0 : 
            ans = "no"
            weight = 1
         #if ans == "other": continue
         if ans == "other":
            weight = 1
         
         newNode = parent, (t.qgloss,ans)
         #print parent, newNode
         #H.add_edge(parent,newNode)
         H.add_edge(parent,newNode,weight=weight)
         parent = newNode

   else:  #python has for... else!
      if(parent == "Emotion"):   # add intermediate node 
         H.add_edge(parent,"LowFrequencyGuesses")
         parent = "LowFrequencyGuesses"

      emotionSynonyms = re.search(r'(\w+)(?:/(\w+))*$',m.emotion() )
      for e in emotionSynonyms.groups():
         if e is not None: H.add_edge(parent,e, weight=20)
      G.add_edges_from(H.edges(data=True))
      
      # path = filter(lambda x: x!="non-yes-no", path)
      # path = filter(lambda x: x!="giveup", path)
      # path.insert(0,"Emotion")
      # path.append(m.emotion)
      # G.add_path(path)

if not sys.argv[1] in G:
   print sys.argv[1], "not found in graph"

print len(G)
# find shortest path between starting point and input
# dijkstra

def dijkstra(g,source,target):
   # initialize
   dist = dict()
   prev = dict()
   for v in g:
      dist[v] = float("inf")  # set the distance to infinity/None
      prev[v] = None          # optimal path from source
   dist[source] = 0
   Q = [v for v in g]
   while Q:
      u = sorted(Q, key=dist.__getitem__)[0]
      if u == target:
         print dist[u]
         print prev[u]
         return dist[u]
      if u==float("inf"): raise ValueError()
      Q.remove(u)
      if u in Q:
         print "wtf"
      for v in g[u]:
         #alt = dist[u] + 1

         alt = dist[u] + g[u][v]['weight']
         if alt < dist[v]: 
            dist[v] = alt
            prev[v] = u
            #decrease key
         

def bellmanFord(g,source,target):
   #this implementation takes a graph, the source, and the target node
   #it modifies the graph by adding distance and predecessor attributes
   
   #initialization
   dist = dict()
   prev = dict()
   for v in g:
      dist[v] = float("inf")  # set the distance to infinity/None
      prev[v] = None          # optimal path from source
   dist[source] = 0

   #relax edges
   for v in g:
      for u,v,w in g.edges(data=True):
         print u,v,w
         sys.exit()
      
   
#bellmanFord(G,("Emotion",), sys.argv[1])
dijkstra(G,("Emotion",), sys.argv[1])

# plt.figure(figsize=(18,18))
# pos=nx.graphviz_layout(G,prog='twopi',root=('Emotion',),args='',)
# nx.draw(G,pos,node_size=10,alpha=0.5,node_color="blue", with_labels=True)
# #nx.draw_graphviz(G)
# nx.write_dot(G,'emo20q.dot')
# #nx.draw(G)
# plt.show()
