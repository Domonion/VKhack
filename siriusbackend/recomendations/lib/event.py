from recomendations import util
from recomendations.util import graph

from mainapp import models
from mainapp.models import User, Event

import datetime






class EventHandler:
    event_graph = graph.read_graph(graph.EVENT_GRAPH)
    subcategory_graph = graph.read_graph(graph.SUBCATEGORY_GRAPH)
    categories = models.get_all_subcategories()

    def get_all_sorted_events(self, user_id):

        class MergedGraphVertex:
            def __init__(self, vertex_type, obj, dist = graph.INFINITY ** 2):
                self.type = vertex_type
                self.object = obj
                self.distance = dist
                self.edges = list()


        now = datetime.datetime.now()
        user = models.User.objects.get(id=user_id)
        vertex = list().append(MergedGraphVertex('user', user, 0))

        user2cats = dict()
        user2subcats = dict()  # get from user

        for cat in self.categories:
            for subcat in cat:
                user2cats[cat] = user2cats.get(cat, 0) + user2subcats[subcat]

        return dict()