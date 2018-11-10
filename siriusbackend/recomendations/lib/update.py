def update_func(graph, queries):
    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    res = dict()
    for k in graph:
        for i in graph:
            for j in graph:
                graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])
    return res
