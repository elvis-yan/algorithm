import sys

def memo(fn):
    cache = {}
    def func(*args):
        try:
            result = cache[args]
        except KeyError:
            cache[args] = result = fn(*args)
        return result
    return func

@memo
def max_min(n, k):
    "return (max, min, num_to_take)"
    if n == 1:
        return 0, 1, 1
    if k >= n - 1:
        return 1, 0, n-1
    for i in range(1, k+1):
        a, b, _ = max_min(n-i, k)
        if a == 0 and b == 1:
            return 1, 0, i
    return 0, 1, 1

def game(n=30, k=3):
    print('#bottles: {}, #once-you-can-take: {}'.format(n, k))
    you = Player('you  ', you_strategy)
    robot = Player('robot', best_strategy)
    while n > 0:
        n = you.play(n, k)
        if n == 0:
            print('You Loose!')
            break
        n = robot.play(n, k)
        if n == 0:
            print('You win!')
            break
        print(n, 'bottles left')


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy

    def play(self, n, k):
        x = self.strategy(n, k)
        print('\t\t{} take {} bottles'.format(self.name, x))
        return n - x

def best_strategy(n, k):
    return max_min(n, k)[2]

def you_strategy(n, k):
    x = int(input('how many bottles do you want to take? '))
    if not 0 < x <= k or x > n:
        raise ValueError("the number({}) you input not appropriate".format(x))
    return x


def test_max_min():
    assert max_min(0, 2) == (1, 0, -1) # special
    assert max_min(1, 2) == (0, 1, 1)
    assert max_min(2, 2) == (1, 0, 1)
    assert max_min(3, 2) == (1, 0, 2)
    assert max_min(4, 2) == (0, 1, 1)
    assert max_min(5, 2) == (1, 0, 1)
    assert max_min(6, 2) == (1, 0, 2)
    assert max_min(7, 2) == (0, 1, 1)
    print('max_min test pass')


if __name__ == '__main__':
    test_max_min()
    if len(sys.argv) > 2:
        n, k = int(sys.argv[1]), int(sys.argv[2])
        game(n, k)
    else:
        game()