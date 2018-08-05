import itertools
import collections


class State:
    def __init__(self, G, boat_size, man, items=None, parent=None, taken=[]):
        self.G = G
        self.boat_size = boat_size
        self.man = man
        self.items = set(G) if items is None else set(items)
        self.parent = parent
        self.taken = taken

    def __eq__(self, o):
        return self.G == o.G and self.boat_size == o.boat_size and\
               self.man == o.man and self.items == o.items

    def __hash__(self):
        l = list(self.items)
        l.sort()
        return hash('-'.join(map(str, [self.man]+l)))

    def __str__(self):
        return '{}, {}'.format(self.man, self.items)

    def is_goal(self):
        return self == State(self.G, self.boat_size, 1)

    def next_states(self):
        for taken in self.what_can_be_taken():
            here = self.items - set(taken)
            if not self.is_conflict(here):
                there = set(self.G) - here
                man = (self.man + 1) % 2
                yield State(self.G, self.boat_size, man, there, parent=self, taken=taken)
        
    def what_can_be_taken(self):
        n = self.boat_size-1 if self.boat_size-1 < len(self.items) else len(self.items)
        for r in range(n, -1, -1): # [n...0]
            for t in itertools.combinations(self.items, r):
                yield t


    def is_conflict(self, items):
        for x in items:
            for y in self.G.get(x, []):
                if y in items:
                    return True
        return False


def path(s):
    return [] if s is None else path(s.parent) + [s]

def search(star, Frontier):
    frontier = Frontier([star])
    explored = set([star])
    while frontier:
        s = frontier.pop()
        if s.is_goal():
            return s
        for s2 in s.next_states():
            if s2 not in explored:
                frontier.add(s2)
                explored.add(s2)

def display(path):
    width = len(', '.join(path[0].G)) + 5
    for s1,s2 in zip(path, path[1:]):
        if s1.man == 0:
            print('{{:<{}}}     [{{}}, {{}}] ->  {{:<{}}}'.format(width, width).format(str(s1), 'man', s2.taken, str(s2)))
        else:
            print('{{:<{}}}  <- [{{}}, {{}}]     {{:<{}}}'.format(width, width).format(str(s2), 'man', s2.taken, str(s1)))

class Queue(collections.deque): add = collections.deque.appendleft
def BFS(star): return search(star, Queue)

def cross_river(G, boat_size):
    star = State(G, boat_size, 0)
    result = BFS(star)
    if result is None:
        print('Cannot do it!')
        return
    display(path(result))


#________________________________________________________________________________________________________________________
# Test

def test_next_states():
    f = State.is_conflict
    ## Mock
    State.is_conflict = lambda s, items: False
    s = State([1,2,3,4], 3, 0)
    items_list = [{1,2},{1,3},{1,4},{2,3},{2,4},{3,4},{1},{2},{3},{4},set()]
    for i,x in enumerate(s.next_states()):
        assert x == State([1,2,3,4], 3, 1, items_list[i])
    s = State([1,2], 3, 0)
    items_list = [{1,2},{1},{2},set()]
    for i,x in enumerate(s.next_states()):
        assert x == State([1,2], 3, 1, items_list[i])
    State.is_conflict = f
    ## ~end
    print('State.next_states test pass.')

def test_is_conflict():
    wolf, goat, cabbage = 'wolf goat cabbage'.split()
    G = {wolf: [goat], goat: [cabbage], cabbage: [goat]}
    s = State(G, 2, 0)
    assert not State(G, 2, 0).is_conflict([])
    assert not State(G, 2, 0).is_conflict([wolf])
    assert not State(G, 2, 0).is_conflict([wolf, cabbage])
    assert s.is_conflict([wolf, goat])
    assert State(G, 2, 0).is_conflict([wolf, goat, cabbage])
    print('State.is_conflict test pass')

def test_is_goal():
    assert State({'a': 1, 'b':2}, 2, 1).is_goal()
    assert not State({'a': 1, 'b':2}, 2, 0).is_goal()
    assert not State({'a': 1, 'b':2}, 2, 1, {'a'}).is_goal()
    print('State.is_goal test pass')

def test_path():
    s = State({}, 0, 0)
    s2 = State({}, 0, 0, parent=s)
    s3 = State({}, 0, 0, parent=s2)
    assert path(s) == [s]
    assert path(s2) == [s, s2]
    assert path(s3) == [s, s2, s3]
    print('State.path test pass')

def test_what_can_be_taken():
    s = State(None, 3, 0, [1,2,3])
    assert list(s.what_can_be_taken()) == [(1,2), (1,3), (2,3), (1,), (2,), (3,), ()]
    s = State(None, 4, 0, [1,2,3])
    assert list(s.what_can_be_taken()) == [(1,2,3), (1,2), (1,3), (2,3), (1,), (2,), (3,), ()]
    print('State.what_can_be_taken pass')

def test():
    test_next_states()
    test_is_conflict()
    test_path()
    test_is_goal()
    test_what_can_be_taken()



if __name__ == '__main__':
    test()
    # wolf, goat, cabbage = 'wolf goat cabbage'.split()
    # G = {wolf:[goat], goat:[cabbage, wolf], cabbage:[goat]}
    # cross_river(G, 2)
    # wolf, goat, cabbage, rabbit = 'wolf goat cabbage rabbit'.split()
    # G = {wolf:[goat, rabbit], goat:[cabbage, wolf], cabbage:[goat, rabbit], rabbit:[wolf, cabbage]}
    # cross_river(G, 3)

    cabbage, goat, rabbit, wolf, goose, mouse, grass, cat, carrot = \
    'cabbage goat rabbit wolf goose mouse grass cat carrot'.split()
    G = {cabbage: [goat, rabbit, mouse],
         goat: [cabbage, carrot, wolf, grass],
         rabbit: [cabbage, carrot, grass, wolf],
         wolf: [goat, rabbit, goose, mouse],
         goose: [wolf, grass],
         mouse: [wolf, cabbage, carrot, cat],
         grass: [goose, rabbit, goat],
         cat: [mouse],
         carrot: [mouse, rabbit, goat],}
    cross_river(G, 5)