from ..util import files_to_graph
import threading

from . import update

from mainapp import models

import datetime

class EventHandler:

    def __init__(self, event_graph_path, subcategory_graph_path, event_add_queries_path,
                 event_set_queries_path, subcategory_queries_path):

        self.event_add_queries_path = event_add_queries_path
        self.event_set_queries_path = event_set_queries_path
        self.subcategory_queries_path = subcategory_queries_path
        self.event_graph_path = event_graph_path
        self.subcategory_graph_path = subcategory_graph_path

        self.event_graph = files_to_graph.read_file(event_graph_path)
        self.subcategory_graph = files_to_graph.read_file(subcategory_graph_path)
        self.categories = models.get_all_subcategories()

        self.subcategories_delta = -5
        self.subcategories_dec = -1

    def eval_time_delta(self, old_event, new_event):
        return -(new_event.finish_time - old_event.finish_time).days()

    def get_all_sorted_events(self, user_id):

        class MergedGraphVertex:
            def __init__(self, vertex_type, obj, dist=files_to_graph.INFINITY ** 2):
                self.type = vertex_type
                self.obj = obj
                self.distance = dist
                self.edges = list()

        def calc_event_edge(weight):
            return weight

        def dj(vert):
            for it in range(len(vert)):
                min_dist = files_to_graph.INFINITY ** 2
                index = -1
                for i, vertex in enumerate(vert):
                    if not vertex.used and vertex.distance < min_dist:
                        min_dist = vertex.distance
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
        user = models.User.objects.get(vk_id=user_id)

        cat2dist = dict()
        cat2subcats = self.categories
        subcat2dist = files_to_graph.get_edges_to_subcategories()
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

    def add_event_add_query(self, event):
        files_to_graph.add_query(self.event_add_queries_path, event.id)

    def add_event_set_query(self, first_event_id, second_event_id, delta):
        query = [first_event_id, second_event_id, delta]
        files_to_graph.add_query(self.event_set_queries_path, query)

    def add_event_set_queries(self, queries):
        files_to_graph.add_query(self.event_set_queries_path, queries)

    def add_subcategory_query(self, first_subcat, second_subcat, delta):
        query = [first_subcat, second_subcat, delta]
        files_to_graph.add_query(self.subcategory_queries_path, query)

    def add_subcategory_queries(self, queries):
        files_to_graph.add_queries(self.subcategory_queries_path, queries)

    def process_event(self, user, event, weight):
        subcats = list(models.EventSubcategories.objects.filter(event=event))
        queries = list()

        for from_subcat in subcats:
            for to_subcat in subcats:
                if from_subcat != to_subcat:
                    queries.append([from_subcat, to_subcat, weight])

        self.add_subcategory_queries(queries)

        now = datetime.datetime.now()
        old_events = [item.event for item in list(models.UserEvents.objects.filter(user=user))
                      if item.event.finish_datetime < now and not item.event.repeatable]
        old_events = sorted(old_events, key=lambda t: t.finish_time)
        queries = [[old_event, event, self.eval_time_delta(old_event, event)] for old_event in old_events]

        self.add_event_set_queries(queries)

    def subscribe(self, user, event):
        self.process_event(user, event, self.subcategories_dec)

    def unsubscribe(self, user, event):
        self.process_event(user, event, -self.subcategories_dec)

    def visit(self, user, event):
        self.process_event(user, event, self.subcategories_delta)

event_handler = EventHandler(files_to_graph.EVENT_GRAPH,
                             files_to_graph.SUBCATEGORY_GRAPH,
                             files_to_graph.EVENT_ADD_QUERIES,
                             files_to_graph.EVENT_SET_QUERIES,
                             files_to_graph.SUBCATEGORY_QUERIES)

# _t = threading.Thread(target=update.updater.do).start()
# _t.join()