def search(start, move_gen, is_goal, Frontier):
    frontier = Frontier([start])
    explored = set([start])
    parent = {start: None}
    gen_path = lambda state: [] if state is None else gen_path(parent[state]) + [state]
    while frontier:
        state = frontier.pop()
        if is_goal(state):
            return gen_path(state)
        for state2 in move_gen(state):
            if state2 not in explored:
                frontier.add(state2)
                explored.add(state2)
                parent[state2] = state

class Queue(list): add = list.append


wolf, goat, cabbage = items = ('wolf', 'goat', 'cabbage')
G = {wolf: goat, goat: (cabbage, wolf), cabbage: goat}


def is_goal(state):
    return state == (1,) + tuple(sorted([wolf, goat, cabbage]))

def move_gen(state):
    man, *here = state
    there = set(items) - set(here)
    for x in here:
        here2 = set(here);   here2.discard(x)
        there2 = set(there); there2.add(x)
        if not is_conflict(here2):
            yield ((man+1)%2, ) + tuple(sorted(there2))
    if not is_conflict(here):
        yield ((man+1)%2, ) + tuple(sorted(there))

def is_conflict(here):
    for x in here:
        for y in G.get(x, []):
            if y in here:
                return True
    return False

def display(path):
    for s1,s2 in zip(result, result[1:]):
        diff = set(s1[1:]) - (set(items) - set(s2[1:]))
        if s1[0] == 0:
            print('{:<30}     [{}, {}] ->  {:<30}'.format(str(s1), 'man', diff, str(s2)))
        else:
            print('{:<30}  <- [{}, {}]     {:<30}'.format(str(s2), 'man', diff, str(s1)))



def test_move_gen():
    global is_conflict
    is_conflict = lambda x: False
    assert set(move_gen((0, wolf, goat, cabbage))) == {(1, goat), (1, cabbage), (1, wolf), (1,)}
    got = move_gen((1, goat))
    got = list(map(set, got))
    got.sort()
    wanted = [{0, cabbage, wolf}, {0, cabbage, wolf, goat}]
    wanted.sort()
    assert got == wanted
    print('move_gen test pass.')


if __name__ == '__main__':
    star = (0,) + tuple(sorted([wolf, goat, cabbage]))
    result = search(star, move_gen, is_goal, Queue)
    display(result)