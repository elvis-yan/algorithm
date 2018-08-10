import random

def least_jump(arr):
    @memo
    def dp(i):
        if i == len(arr) - 1:
            return 0
        return 1 + min(dp(i+d) for d in range(1, arr[i]+1) if i+d < len(arr))
    return dp(0)

def memo(fn):
    cache = {}
    def func(arg):
        try:
            result = cache[arg]
        except KeyError:
            cache[arg] = result = fn(arg)
        return result
    return func

def least_jump_iteratively(arr):
    T = [0 for _ in arr]
    for i in reversed(range(len(T)-1)):
        T[i] = 1 + min(T[i+d] for d in range(1, arr[i]+1) if i+d < len(arr))
    return T

def reconstruct_path(T):
    path = [0]
    x = T[0]
    for (i,y) in enumerate(T[1:], 1):
        if x == y + 1:
            path.append(i)
            x = y
    return path


def test():
    arr = [3, 2, 3, 1, 1, 4]
    assert least_jump(arr) == 2
    print('test pass.')

def random_arr(n=10):
    return [random.randint(1, 5) for _ in range(n)]


if __name__ == '__main__':
    # test()
    arr = random_arr(30)
    print(arr)
    # print(least_jump(arr))
    T = least_jump_iteratively(arr)
    print(T[0])
    print(reconstruct_path(T))