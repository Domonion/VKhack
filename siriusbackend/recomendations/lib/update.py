from recomendations.util import graph


def update_subtags_graph(graph, queries):
    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    res = graph
    for k in graph:
        for i in graph:
            for j in graph:
                res[i][j] = min(res[i][j], res[i][k] + res[k][j])
    return res


def update_events_graph(event_graph, new_events):
    for new_event in new_events:
        tmp_dist = dict()
        for old_event in event_graph:
            event_graph[old_event.id][new_event.id] = graph.INFINITY
            tmp_dist[old_event.id] = graph.INFINITY
        event_graph[new_event.id] = tmp_dist
