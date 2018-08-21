from union_set import DisjointSet
from graph import parse, Edge
from queue import *

def kruskal(G):
    US = {}
    for node in G.nodes:
        US[node] = DisjointSet(node)
    X = []
    for edge in sorted(G.edges(), key=lambda e: e.weight):
        src, dest = edge.src, edge.dest
        if US[src].find() != US[dest].find():
            X.append(edge)
            US[src].union(US[dest])
    return X

def prim(G):
    inf = float('inf')
    for node in G.nodes:
        node.cost = inf
        node.prev = None
    node.cost = 0 #pick any initail node

    H = makequeue(G.nodes)
    while H:
        u = deletemin(H)
        for edge in G.get_edges(u):
            v, w = edge.dest, edge.weight
            if v in H and v.cost > w:
                v.cost = w
                v.prev = u
                decreasekey(H, v)
    return edges(set(G.nodes))

def edges(nodes):
    X = []
    while nodes:
        dest = nodes.pop()
        if dest.prev is None:
            continue
        src, weight = dest.prev, dest.cost
        X.append(Edge(src, dest, weight))
    return X


def demo_graph():
    '''
    A -- 1 -- C -- 3 -- E
    |       / |      /  |
    2    2    2    3    1
    |  /      |  /      |  
    B -- 1 -- D -- 4 -- F
    '''

    s = '''{
            'A': [('B', 2), ('C', 1)],
            'B': [('A', 2), ('C', 2), ('D', 1)],
            'C': [('A', 1), ('B', 2), ('D', 2), ('E', 3)],
            'D': [('B', 1), ('C', 2), ('E', 3), ('F', 4)],
            'E': [('C', 3), ('D', 3), ('F', 1)],
            'F': [('D', 4), ('E', 1)]
            }'''
    return parse(s)


G = demo_graph()
X = kruskal(G)
print(X)
print()
X = prim(G)
print(X)
