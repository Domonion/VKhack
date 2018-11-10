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

        def dj(vert):
            for it in range(len(vert)):
                mindist = graph.INFINITY ** 2
                index = -1
                for i, vertex in enumerate(vert):
                    if not vertex.used and vertex.distance < mindist:
                        mindist = vertex.distance
                        index = i
                if index == -1:
                    break
                vert[index].used = 1
                for edge in vert[index].edges:
                    to = edge[0]
                    weight = edge[1]
                    vert[to].distance = min(vert[to].distance, vert[index] + weight)

            result = [vertex.obj for vertex in vert if vertex.type == 'event']
            return sorted(result, key=lambda t: t.distance)

        now = datetime.datetime.now()
        user = models.User.objects.get(id=user_id)

        cat2dist = dict()
        cat2subcats = self.categories
        subcat2dist = dict()  # get from user
        subcat2events = dict()

        for cat in cat2subcats:
            for subcat in cat2subcats[cat]:
                cat2dist[cat] = cat2dist.get(cat, 0) + subcat2dist[subcat]
                subcat2events[subcat] = set()

        dj_graph = list()
        dj_graph.append(MergedGraphVertex('user', user, 0))
        for cat in cat2dist:
            dj_graph[0].edges.append((len(dj_graph), cat2dist[cat]))  # user->cat edges
            dj_graph.append(MergedGraphVertex('category', cat))
        for subcat in subcat2dist:
            dj_graph.append(MergedGraphVertex('subcategory', subcat))
        for item in list(models.Event.objects.all()):
            if item.start_datetime > now:
                dj_graph.append(MergedGraphVertex('event', item))
                
        for item in list(models.EventSubcategories.objects.all()):
            if item.event.start_datetime > now:
                subcat2events[item.subcategory].add(item.event)
        
        for i, v in enumerate(dj_graph):
            for j, u in enumerate(dj_graph):
                if v.type == 'subcategory' and u.type == 'event':
                    if u.obj in subcat2events[v.obj]:  # subcategory->event edges
                        v.edges.append((j, 0))
                if v.type == 'subcategory' and u.type == 'subcategory':  # subcategory->subcategory edges
                    v.edges.append((j, self.subcategory_graph[v.obj][u.obj]))
                if v.type == 'category' and u.type == 'subcategory':  # category->subcategory edges
                    v.edges.append((j, subcat2dist[u.obj]))
                if v.type == 'event' and u.type == 'event':  # event->event edges
                    v.edges.append((j, calc_event_edge(self.event_graph[v.obj.id][u.obj.id])))

        return dj(dj_graph)

