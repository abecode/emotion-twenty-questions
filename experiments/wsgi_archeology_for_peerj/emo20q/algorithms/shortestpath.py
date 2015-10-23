#!/usr/bin/python

from emo20q.data.base import HumanHumanTournament
import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import sys
from collections import defaultdict


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
         #print dist[u]
         #print prev[u]
         return dist[u],[x for x in unwind(prev[u])]
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

def unwind(wound):
   if len(wound)==1:
      yield wound
   else:
      left,right = wound
      for x in unwind(left):
         yield x
      yield right
      
   
#bellmanFord(G,("Emotion",), sys.argv[1])
if __name__ == "__main__":
   try: sys.argv[1]
   except:   
      print "no argument given"
      sys.exit(1)

   from  emo20q.models.describergraph import DescriberGraph

   G = DescriberGraph()
   if not sys.argv[1] in G:
      print sys.argv[1], "not found in graph"
      
   print len(G)
   cost,path = dijkstra(G,("Emotion",), sys.argv[1])
   print cost
   for x in path:
      print x
