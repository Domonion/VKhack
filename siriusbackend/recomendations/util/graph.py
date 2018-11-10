import json
import os
from filelock import FileLock

from mainapp import models

INFINITY = 10**12
HOME = os.environ['HOME']
GRAPH_DIR = 'data'
SUBCATEGORY_GRAPH_FILE = 'subcategories_graph.json'
EVENT_GRAPH_FILE = 'events_graph.json'
SUBCATEGORY_GRAPH = os.path.join(HOME, GRAPH_DIR, SUBCATEGORY_GRAPH_FILE)
EVENT_GRAPH = os.path.join(HOME, GRAPH_DIR, EVENT_GRAPH_FILE)
USER_SUBCATEGORIES_EDGES = os.path.join(HOME, GRAPH_DIR)


def read_file(file_path):
    file = open(file_path, 'r')
    graph = json.loads(file.read())
    file.close()
    return graph


def write_graph(file_path, graph):
    with FileLock(file_path):
        file = open(file_path, 'w')
        file.write(json.dumps(graph, separators=(',', ':')))
        file.close()


def clear_file(file_path):
    with FileLock(file_path):
        open(file_path, 'w').close()


def init_subcategories_graph(file_path):
    global INFINITY

    categories = models.get_all_subcategories()

    subcats_cnt = 0
    for cat in categories:
        for subcat in cat:
            subcats_cnt += len(subcat)

    graph = [[INFINITY] * subcats_cnt for i in range(subcats_cnt)]
    for i in range(subcats_cnt):
        graph[i][i] = 0

    write_graph(file_path, graph)


def init_edges_from_user_to_subcategories(file_path):
    categories = models.Subcategories.objects.all()
    size = max([x.id for x in categories]) + 1
    with open(os.path.join(USER_SUBCATEGORIES_EDGES, file_path), "wb") as file:
        file.write(json.dumps([INFINITY] * size))


def get_edges_to_subcategories(user):
    filename = user.subcategories_file
    with open(os.path.join(USER_SUBCATEGORIES_EDGES, filename), "rb") as file:
        array = json.loads(file.read())
    return {subcategory.name: array[i] for subcategory, i in zip(models.Subcategories.objects.order_by("id").all(),
                                                                 range(models.Subcategories.objects.count()))}


def update_graph(graph_file_path, queries_file_path, update_func):
    graph = read_file(graph_file_path)
    queries = read_file(queries_file_path)

    result_graph = update_func(graph, queries)

    clear_file(queries_file_path)
    write_graph(graph_file_path, result_graph)
