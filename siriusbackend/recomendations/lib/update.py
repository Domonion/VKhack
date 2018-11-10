
from siriusbackend.recomendations import util
from siriusbackend.recomendations.util import graph

from siriusbackend.mainapp import models
from siriusbackend.mainapp.models import *

#graph - dict dict int
#queris - list, 3 int

def update_func(graph, queries):
    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    res = dict()
    for k in graph:
        for i in graph:
            for j in graph:
                graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])
    return res
