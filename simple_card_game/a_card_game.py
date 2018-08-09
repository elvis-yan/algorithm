# cards = [48, 69, 33, 34, 29, 89, 65, 20, 25, 66]
# two player A, B
# take a card from the head or the end of the card-list
# the one who got larger sum-of-card-values win


import random

def memo(fn):
    cache = {}
    def _func(x):
        key = tuple(x)
        try:
            result = cache[key]
        except KeyError:
            cache[key] = result = fn(x)
        return result
    return _func

@memo
def max_min(cards):
    "return maximum value for self and minimum value for opponent"
    if len(cards) == 0:
        return 0, 0
    elif len(cards) == 1:
        return cards[0], 0
    a1, b1 = max_min(cards[1:])
    a2, b2 = max_min(cards[:-1])
    if cards[0] + b1 > cards[-1] + b2:
        return cards[0]+b1, a1
    else:
        return cards[-1]+b2, a2

def gen_cards(n=10):
    cards = list(range(1, 100)) if n < 100 else list(range(1, n+1))
    random.shuffle(cards)
    return cards[:n]

def max_min_iteratively(cards):
    if len(cards) == 0:
        return 0, 0
    T = [[(0,0) for _ in range(len(cards))] for _ in range(len(cards))]
    for j in range(len(cards)):
        T[j][j] = cards[j], 0
        for i in reversed(range(0, j)):
            a1, b1 = T[i+1][j]
            a2, b2 = T[i][j-1]
            if b1 + cards[i] > b2 + cards[j]:
                T[i][j] = b1+cards[i], a1
            else:
                T[i][j] = b2+cards[j], a2
    return T
    

cards = gen_cards(60)
print(cards)
print(max_min(cards))
print(max_min_iteratively(cards)[0][len(cards)-1])