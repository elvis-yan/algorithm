from graph import parse, Edge
from queue import *

def dijkstra(G, s):
    inf = float('inf')
    for node in G.nodes:
        node.cost = inf
        node.prev = None
    s.cost = 0

    H = makequeue(G.nodes)
    X = {s}
    while H:
        u = deletemin(H)
        for edge in G.get_edges(u):
            v, w = edge.dest, edge.weight
            if v.cost > u.cost + w:
                v.cost = u.cost + w
                v.prev = u
                decreasekey(H, v)
                X.add(v)
    return list(X)



def path(G, node):
    return path(G, node.prev) + [Edge(node.prev, node, node.cost - node.prev.cost)] if node.prev is not None else []

def demo_grahp():
    s = '''{
            'A': [('B', 4), ('C', 2)],
            'B': [('C', 3), ('D', 2), ('E', 3)],
            'C': [('B', 1), ('D', 4), ('E', 5)],
            'D': [],
            'E': [('D', 1)]
            }'''
    return parse(s)

G = demo_grahp()
X = dijkstra(G, G.get_node('A'))
X.sort(key=lambda n: n.cost)
for n in X:
    print(n, n.cost, path(G, n))