from collections import OrderedDict

from recomendations import util
from recomendations.util import graph

from mainapp import models
from mainapp.models import *

import datetime






class EventHandler:
    event_graph = graph.read_graph(graph.EVENT_GRAPH)
    subcategory_graph = graph.read_graph(graph.SUBCATEGORY_GRAPH)
    categories = models.get_all_subcategories()

    def get_all_sorted_events(self, user_id):

        class MergedGraphVertex:
            def __init__(self, vertex_type, obj, dist = graph.INFINITY ** 2):
                self.type = vertex_type
                self.obj = obj
                self.distance = dist
                self.edges = list()

        def calc_event_edge(weight):
            return weight

        now = datetime.datetime.now()
        user = models.User.objects.get(id=user_id)

        cat2dist = dict()
        cat2subcats = self.categories
        subcat2dist = dict() # get from user
        subcat2events = dict()

        for cat in cat2subcats:
            for subcat in cat2subcats[cat]:
                cat2dist[cat] = cat2dist.get(cat, 0) + subcat2dist[subcat]
                subcat2events[subcat] = set()

        graph = list()
        graph.append(MergedGraphVertex('user', user, 0))
        for cat in cat2dist:
            graph[0].edges.append((len(graph), cat2dist[cat]))  # user->cat edges
            graph.append(MergedGraphVertex('category', cat)) 
        for subcat in subcat2dist:
            graph.append(MergedGraphVertex('subcategory', subcat))
        for item in list(models.Event.objects.all()):
            if item.start_datetime > now:
                graph.append(MergedGraphVertex('event', item))
                
        for item in list(models.EventSubcategories.objects.all()):
            if item.event.start_datetime > now:
                subcat2events[item.subcategory].add(item.event)
        
        for i, v in enumerate(graph):
            for j, u in enumerate(graph):
                if v.type == 'subcategory' and u.type == 'event':
                    if u.obj in subcat2events[v.obj]:  # subcategory->event edges
                        v.edges.append((j, 0))
                if v.type == 'subcategory' and u.type == 'subcategory':  # subcategory->subcategory edges
                    v.edges.append((j, self.subcategory_graph[v.obj][u.obj]))
                if v.type == 'category' and u.type == 'subcategory':  # category->subcategory edges
                    v.edges.append((j, subcat2dist[u.obj]))
                if v.type == 'event' and u.type == 'event':  # event->event edges
                    v.edges.append((j, calc_event_edge(self.event_graph[v.obj][u.obj])))

        return dict()

