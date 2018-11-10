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

    subcats = list()
    for cat in categories:
        for subcat in cat:
            subcats.append(subcat)

    graph = dict()

    for i, src_subcat in enumerate(subcats):
        graph[src_subcat] = dict()
        for j, dst_subcat in enumerate(subcats):
            graph[src_subcat][dst_subcat] = INFINITY if i != j else 0

    write_graph(file_path, graph)


def update_graph(graph_file_path, queries_file_path, update_func):
    graph = read_file(graph_file_path)
    queries = read_file(queries_file_path)

    result_graph = update_func(graph, queries)

    clear_file(queries_file_path)
    write_graph(graph_file_path, result_graph)
