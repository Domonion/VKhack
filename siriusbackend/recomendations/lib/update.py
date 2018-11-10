import threading

from recomendations.util import files_to_graph
import time


def update_graph_set(graph, queries):
    if not queries:
        return graph

    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    for k in graph:
        for i in graph:
            for j in graph:
                graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])
    return graph


def update_graph_add(event_graph, new_events_id):
    for new_event_id in new_events_id:
        tmp_dict = dict()
        for old_event_id in event_graph:
            event_graph[old_event_id][new_event_id] = files_to_graph.INFINITY
            tmp_dict[old_event_id] = files_to_graph.INFINITY
        tmp_dict[new_event_id] = 0
        event_graph[new_event_id] = tmp_dict
    return event_graph


def update_graph(graph_file_path, queries_file_path, update_func):
    graph = files_to_graph.read_file(graph_file_path)
    queries = files_to_graph.read_file(queries_file_path)

    result_graph = update_func(graph, queries)

    files_to_graph.clear_file(queries_file_path)
    files_to_graph.write_file(graph_file_path, result_graph)


class Updater:
    period = 30  # seconds
    need_stop = False

    def do_once(self):
        update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_ADD_QUERIES, update_graph_add)
        update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_SET_QUERIES, update_graph_set)
        update_graph(files_to_graph.SUBCATEGORY_GRAPH, files_to_graph.SUBCATEGORY_QUERIES, update_graph_set)

    def do(self):
        while not self.need_stop:
            print("Start serving updates...")

            time.sleep(self.period)

            update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_ADD_QUERIES, update_graph_add)
            update_graph(files_to_graph.EVENT_GRAPH, files_to_graph.EVENT_SET_QUERIES, update_graph_set)
            update_graph(files_to_graph.SUBCATEGORY_GRAPH, files_to_graph.SUBCATEGORY_QUERIES, update_graph_set)


    def stop(self):
        self.need_stop = True

updater = Updater()


def _kek_target():
    while True:
        # try:
        current_alive_thread = threading.Thread(target=updater.do)
        current_alive_thread.start()
        current_alive_thread.join()
        # except Exception:
        #     pass
        # time.sleep(1)


_kek_thread = threading.Thread(target=updater.do)
_kek_thread.start()
