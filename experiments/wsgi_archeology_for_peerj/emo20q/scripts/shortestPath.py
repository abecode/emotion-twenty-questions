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


from  emo20q.models.describergraph import DescriberGraph
from emo20q.algorithms.shortestpath import dijkstra,bellmanFord

G = DescriberGraph()
if not sys.argv[1] in G:
   print sys.argv[1], "not found in graph"

print len(G)
print dijkstra(G,("Emotion",), sys.argv[1])
#bellmanFord(G,("Emotion",), sys.argv[1])

# plt.figure(figsize=(18,18))
# pos=nx.graphviz_layout(G,prog='twopi',root=('Emotion',),args='',)
# nx.draw(G,pos,node_size=10,alpha=0.5,node_color="blue", with_labels=True)
# #nx.draw_graphviz(G)
# nx.write_dot(G,'emo20q.dot')
# #nx.draw(G)
# plt.show()
