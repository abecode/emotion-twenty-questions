#!/usr/bin/python

from emo20q.models.describergraph import DescriberGraph
from emo20q.nlp import GenerateDeclarative
from emo20q.algorithms.shortestpath  import dijkstra

class DescriberAgent(object):
    dialogGraph = DescriberGraph()
    lexicalAccess = GenerateDeclarative()
    pass



if __name__ == "__main__":
    import doctest
    import sys
    doctest.testmod()
    
    agent = DescriberAgent()

    if len(sys.argv) > 1:
        if sys.argv[1] not in agent.dialogGraph:
            raise KeyError, "%s not found"%sys.argv[1]
        cost,path = dijkstra(agent.dialogGraph,("Emotion",),sys.argv[1])
        print cost
        path=path[1:]
        for x in path:
            #print x
            print agent.lexicalAccess(x[0],x[1])
    
