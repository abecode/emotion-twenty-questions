#!/usr/bin/python

from emo20q.data.base import HumanHumanTournament

import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from collections import defaultdict
import re

class DialogGraph(nx.DiGraph):
   def __new__(self, annotationFile="../annotate/emo20q.txt"):
      # read in tournament, do some testing, get some stats
      tournament = HumanHumanTournament(annotationFile)
      
      #count turns in a dict, for pruning
      qcounts = defaultdict(int)
      for m in tournament.matches():
         for t in m.turns(): 
            qcounts[t.qgloss]+=1 

      #create graph
      G = nx.DiGraph()
      G.add_node("Emotion")

      #add emo20q data to graph
      for m_idx,m in enumerate(tournament.matches()):
         H = nx.DiGraph()
         parent = "Emotion"
         edge = "yes"
         H.add_node(parent)
         for t in m.turns():
            if(qcounts[t.qgloss]>1):
               #deal with guesses:
               guess = re.search(r'^e==(\w+)$',t.qgloss )
               if(guess):
                  H.add_edge(parent,guess.group(1))
                  #G.add_nodes_from(H)
                  continue
               #deal with questions
               if (t.qgloss.find("non-yes-no")==0): continue
               if (t.qgloss.find("giveup")==0): continue
               ans = "other" 
               if t.agloss.find("yes") == 0 : ans = "yes" 
               if t.agloss.find("no") == 0 : ans = "no"
               #if ans == "other": continue
               newNode = (t.qgloss,ans)
               H.add_edge(parent,newNode)
               parent = newNode
               
         else:  #python has for... else!
            # if(parent == "Emotion"):   # add intermediate node 
            #    H.add_edge(parent,"LowFrequencyGuesses")
            #    parent = "LowFrequencyGuesses"
               
            emotionSynonyms = re.search(r'(\w+)(?:/(\w+))*$',m.emotion() )
            for e in emotionSynonyms.groups():
               if e is not None: H.add_edge(parent,e)
            G.add_edges_from(H.edges())
      return G

if __name__ == "__main__":
   G = DialogGraph()
   plt.figure(figsize=(18,18))
   pos=nx.graphviz_layout(G,prog='twopi',root='Emotion',args='',)
   nx.draw(G,pos,node_size=10,alpha=0.5,node_color="blue", with_labels=True)
   #nx.draw_graphviz(G)
   #nx.write_dot(G,'emo20q.dot')
   #nx.draw(G)
   plt.show()
