import json
import os
from filelock import FileLock

from mainapp import models

INFINITY = 10**12

HOME = os.environ['HOME']
GRAPH_DIR = 'data'
USER_DIR = 'users'

USER_SUBCATEGORIES_DIR = os.path.join(GRAPH_DIR, USER_DIR)

SUBCATEGORY_GRAPH_FILE = 'subcategories_graph.json'
EVENT_GRAPH_FILE = 'events_graph.json'

SUBCATEGORY_GRAPH = os.path.join(HOME, GRAPH_DIR, SUBCATEGORY_GRAPH_FILE)
EVENT_GRAPH = os.path.join(HOME, GRAPH_DIR, EVENT_GRAPH_FILE)

SUBCATEGORY_QUERIES_FILE = 'subcategories_queries.json'
EVENT_ADD_QUERIES_FILE = 'events_add_queries.json'
EVENT_SET_QUERIES_FILE = 'events_set_queries.json'

SUBCATEGORY_QUERIES = os.path.join(HOME, GRAPH_DIR, SUBCATEGORY_QUERIES_FILE)
EVENT_ADD_QUERIES = os.path.join(HOME, GRAPH_DIR, EVENT_ADD_QUERIES_FILE)
EVENT_SET_QUERIES = os.path.join(HOME, GRAPH_DIR, EVENT_SET_QUERIES_FILE)


def read_file(file_path):
    file = open(file_path, 'r')
    graph = json.loads(file.read())
    file.close()
    return graph


def write_file(file_path, item):
    with FileLock(file_path):
        file = open(file_path, 'w')
        file.write(json.dumps(item, separators=(',', ':')))
        file.close()


def add_query(file_path, query):
    queries = read_file(file_path)
    if not queries:
        queries = list()
    queries.append(query)
    write_file(file_path, queries)


def add_queries(file_path, queries):
    old_queries = read_file(file_path)
    if not old_queries:
        old_queries = list()
    old_queries.extend(queries)
    write_file(file_path, old_queries)


def clear_file(file_path):
    with FileLock(file_path):
        open(file_path, 'w').close()


def init_subcategories_graph(file_path):

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

    write_file(file_path, graph)


def init_edges_from_user_to_subcategories(file_path):
    subcategories = models.Subcategories.objects.all()
    with open(os.path.join(USER_SUBCATEGORIES_DIR, file_path), "w") as file:
        result = {x: INFINITY for x in subcategories}
        file.write(json.dumps(result))


def get_edges_to_subcategories(user):
    filename = user.subcategories_file
    with open(os.path.join(USER_SUBCATEGORIES_DIR, filename), "r") as file:
        return json.loads(file.read())



