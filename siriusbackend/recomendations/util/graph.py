import json
from filelock import FileLock

from mainapp import models

INFINITY = 10**12


def read_file(file_path):
    file = open(file_path, 'r')
    graph = json.loads(file.read())
    file.close()
    return graph


def write_graph(file_path, graph):
    with FileLock(file_path):
        file = open(file_path, 'w')
    json.dumps(graph, separators=(',', ':'))
    file.close()


def clear_file(file_path):
    with FileLock(file_path):
        open(file_path, 'w').close()


def init_subcategories_graph(file_path):
    global INFINITY

    categories = models.get_all_categories()

    subcats_cnt = 0
    for cat in categories:
        for subcat in cat:
            subcats_cnt += len(subcat)

    graph = [[INFINITY] * subcats_cnt for i in range(subcats_cnt)]
    for i in range(subcats_cnt):
        graph[i][i] = 0

    write_graph(file_path, graph)


def update_graph(graph_file_path, queries_file_path, update_func):
    graph = read_file(graph_file_path)
    queries = read_file(queries_file_path)

    result_graph = update_func(graph, queries)

    clear_file(queries_file_path)
    write_graph(graph_file_path, result_graph)
