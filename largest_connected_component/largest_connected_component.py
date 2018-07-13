import collections
import random


class Graph:
    def __init__(self, s):
        M = list(map(list, s.split()))
        self.M = self._init(M)

    def _init(self, M):
        for i,row in enumerate(M):
            for j, v in enumerate(row):
                M[i][j] = Node(v, (i, j), self)
        return M

    def __str__(self):
        return '\n'.join(map(''.join, (map(str, nodes) for nodes in self.M)))
    __repr__ = __str__

    def bfs(self, node):
        return self._search(node, Queue())             

    def dfs(self, node):
        return self._search(node, Stack())

    def _search(self, node, frontier):
        explored = set()
        frontier.put(node)
        while len(frontier) > 0:
            n = frontier.pop()
            explored.add(n)
            yield n
            for n2 in n.neighbours():
                if n2 not in explored and n2 not in frontier:
                    frontier.put(n2)


class Queue(collections.deque): put = collections.deque.appendleft
class Stack(list):              put = list.append    

               
class Node:
    def __init__(self, color, position, graph):
        self.color   = color
        self.position = position
        self.graph   = graph

    def __str__(self): return str(self.color)
    __repr__ = __str__

    def _neighbours(self):
        i, j = self.position
        m, n = len(self.graph.M), len(self.graph.M[0])
        positions = filter(lambda t: 0 <= t[0] < m and 0 <= t[1] < n,
                           [(i, j-1), (i, j+1), (i-1, j), (i+1, j)])
        for i,j in positions:
            yield self.graph.M[i][j]

    def neighbours(self):
        return filter(lambda n: n.color == self.color, self._neighbours())

#_____________________________________________________________________________    
# Tests for Graph

def test__neighbours():
    s = '0012 0121 2111'
    g = Graph(s)
    ts = {
        (0, 0): [(0, 1), (1, 0)],
        (1, 1): [(1, 0), (1, 2), (0, 1), (2, 1)],
        (2, 2): [(2, 1), (2, 3), (1, 2)]
        }
    for i,j in ts:
        assert ts[(i,j)] == [n.position for n in g.M[i][j]._neighbours()]
    return 'Node._neighbours() tests pass.'

def test__search():
    s = '0012 0121 2111'
    g = Graph(s)
    n = g.M[2][2]
    l1 = [(2, 2), (2, 3), (1, 3), (2, 1), (1, 1)]
    l2 = [(2, 2), (2, 1), (2, 3), (1, 1), (1, 3)]
    assert [n2.position for n2 in g.dfs(n)] == l1
    assert [n2.position for n2 in g.bfs(n)] == l2
    return 'Graph._search tests pass.'

#_____________________________________________________________________________

def random_graph(m=7, n=9, num_colors=3):
    colors = list(range(num_colors))
    l = []
    for _ in range(m):
        for _ in range(n):
            l.append(str(random.choice(colors)))
        l.append('\n')
    s = ''.join(l)
    return Graph(s)

def solve(graph, key=max):
    nodes = set(node for row in graph.M for node in row)
    connect_components = []
    while len(nodes) > 0:
        s = set(graph.dfs(nodes.pop()))
        connect_components.append(s)
        nodes -= s
    return max(connect_components, key=len)
    
def display_result(graph):
    all_nodes = set(node for row in graph.M for node in row)
    nodes = solve(graph)
    print('#{}'.format(len(nodes)))
    print(graph)
    print('=' * len(graph.M[0]))
    for n in all_nodes:
        if n in nodes:
            n.color = 'X'
        else:
            n.color = '.'
    print(graph)


if __name__ == '__main__':
##    print(test__neighbours())
##    print(test__search())
    display_result(random_graph(20, 100, 3))
