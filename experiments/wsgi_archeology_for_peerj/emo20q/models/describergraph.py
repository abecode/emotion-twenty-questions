#!/usr/bin/python

from emo20q.data.base import HumanHumanTournament,HumanComputerTournament
import emo20q.nlp as nlp
import networkx as nx
from networkx import graphviz_layout
import matplotlib.pyplot as plt
from collections import defaultdict
import re



class DescriberGraph(nx.DiGraph):
   """
   This is like the dialog graph but it has weights that affect the
   description that is generated
   """

   def __new__(self, annotationFile="../annotate/emo20q.txt"):
      # read in tournament, do some testing, get some stats
      tournament = HumanHumanTournament(annotationFile) + HumanComputerTournament()
      
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
         parent = ("Emotion",)
         edge = "yes"
         H.add_node(parent)
         for t in m.turns():
            if(qcounts[t.qgloss]>0):
               #deal with guesses:
               guess = re.search(r'^e==(\w+)(\|\|.*)*$',t.qgloss )
               if(guess):
                  #if re.search(r'close', t.a ): #connect a close guess
                  #   H.add_edge(parent,guess.group(1), weight=20)
                  continue
               #deal with questions
               if (t.qgloss.find("non-yes-no")==0): continue
               if (t.qgloss.find("clarification")==0): continue
               if (t.qgloss.find("giveup")==0): continue
               ans = "other" 
               # #use nlp module here!
               # if t.a.find("yes") == 0 : 
               #    ans = "yes" 
               #    weight = -5
               # if t.a.find("no") == 0 : 
               #    ans = "no"
               #    weight = 2
               # if ans == "other": 
               #    weight = 5
               if nlp.classifyYN(t.a) == 1 : 
                  ans = "yes" 
                  weight = -1
               if nlp.classifyYN(t.a) == -1 : 
                  ans = "no"
                  weight = 0
               if ans == "other": 
                  weight = 1
               
               newNode = parent, (t.qgloss,ans)
               H.add_edge(parent,newNode,weight=weight)
               parent = newNode
               
               if t.qgloss == "e.valence==positive" and m.emotion() == "happiness" and ans == "no":
                  print "wtf!"
                  print t.qgloss, t.a, m.emotion()
                  for t in m.turns():
                     print t.qgloss, t.a
         else:  #python has for... else!
            #if(parent == "Emotion"):   # add intermediate node 
            #   H.add_edge(parent,"LowFrequencyGuesses")
            #   parent = "LowFrequencyGuesses"
               
            emotionSynonyms = re.search(r'(\w+)(?:/(\w+))*$',m.emotion() )
            for e in emotionSynonyms.groups():
               if e is not None: H.add_edge(parent,e, weight=20)
            G.add_edges_from(H.edges(data=True))
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
