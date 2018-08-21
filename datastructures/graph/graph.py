class Node:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, node):
        return self.name == node.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Node({})'.format(self.name)


class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __str__(self):
        return '{} -- {} --> {}'.format(self.src, self.weight, self.dest)

    def __repr__(self):
        return 'Edge({}, {}, {})'.format(self.src, self.dest, self.weight)


class Graph:
    def __init__(self):
        self.nodes = {} # node -> [(node, weight)...]

    def add_node(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate {!r}'.format(node))
        self.nodes[node] = []

    def add_edge(self, edge):
        src, dest, weight = edge.src, edge.dest, edge.weight
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in Graph')
        self.nodes[src].append((dest, weight))

    def neighbours(self, node):
        return [n for n,w in self.nodes[node]]

    def edges(self):
        result = []
        for src in self.nodes:
            for dest,weight in self.nodes[src]:
                result.append(Edge(src, dest, weight))
        return result

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        raise NameError(name)

    def get_edges(self, node):
        if node not in self.nodes:
            raise ValueError('Node not in Graph')
        result = []
        for dest,weight in self.nodes[node]:
            result.append(Edge(node, dest, weight))
        return result
    
    def __str__(self):
        return '\n'.join(map(str, self.edges()))


def parse(s):
    ''' "{'A': [('B', 2), ('C', 3)]}" -> Graph '''
    def add_node(graph, name):
        graph.add_node(Node(name))

    def add_edge(graph, name1, name2, weight=1):
        graph.add_edge(
            Edge(
                graph.get_node(name1),
                graph.get_node(name2),
                weight))
    dic = eval(s)
    g = Graph()
    for name in dic:
        add_node(g, name)
    for src in dic:
        for dest, weight in dic[src]:
            add_edge(g, src, dest, weight)
    
    return g