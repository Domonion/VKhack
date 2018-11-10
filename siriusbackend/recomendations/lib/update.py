from recomendations.util import files_to_graph
import time


def update_graph_set(graph, queries):
    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    res = graph
    for k in graph:
        for i in graph:
            for j in graph:
                res[i][j] = min(res[i][j], res[i][k] + res[k][j])
    return res


def update_graph_add(event_graph, new_events):
    for new_event in new_events:
        tmp_dist = dict()
        for old_event in event_graph:
            event_graph[old_event.id][new_event.id] = files_to_graph.INFINITY
            tmp_dist[old_event.id] = files_to_graph.INFINITY
        event_graph[new_event.id] = tmp_dist


def update_graph(graph_file_path, queries_file_path, update_func):
    graph = files_to_graph.read_file(graph_file_path)
    queries = files_to_graph.read_file(queries_file_path)

    result_graph = update_func(graph, queries)

    files_to_graph.clear_file(queries_file_path)
    files_to_graph.write_file(graph_file_path, result_graph)


class Updater:
    period = 30  # seconds
    need_stop = False

    def do(self):
        while not self.need_stop:
            update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_ADD_QUERIES, update_graph_add)
            update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_SET_QUERIES, update_graph_set)
            update_graph(files_to_graph.SUBCATEGORY_GRAPH, files_to_graph.SUBCATEGORY_QUERIES, update_graph_set)

            time.sleep(self.period)

    def stop(self):
        self.need_stop = True
