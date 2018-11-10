def update_func(graph, queries):
    for tpl in queries:
        graph[tpl[0]][tpl[1]] += tpl[2]
        graph[tpl[1]][tpl[0]] += tpl[2]
    res = graph
    for k in graph:
        for i in graph:
            for j in graph:
                res[i][j] = min(res[i][j], res[i][k] + res[k][j])
    return res
