# cards = [48, 69, 33, 34, 29, 89, 65, 20, 25, 66]
# two player A, B
# take a card from the head or the end of the card-list
# the one who got larger sum-of-card-values win


import random
import os
import sys

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
    

def reconstruct_path(cards, T):
    path = []
    i, j = 0, len(cards)-1
    while i <= j:
        if i == j:
            path.append(0)
            break
        _, b = T[i+1][j]
        if T[i][j][0] == b+cards[i]:
            path.append(0) # head
            i += 1
        else:
            path.append(1) # tail
            j -= 1
    return path

def strategy(cards):
    T = max_min_iteratively(cards)
    i, j = 0, len(cards)-1
    if i == j:
        return 0
    # i < j
    _, b = T[i+1][j]
    if T[i][j][0] == b + cards[i]:
        return 0
    else:
        return 1

def game(n=20):
    cards = gen_cards(n)
    cards2 = cards[:]
    you = int(input('play as player1 or player2[1/2]? ')) # it's dangerous but simple

    if you == 1:
        player1 = Player('you  ', you_strategy)
        player2 = Player('robot')
    else:
        player1 = Player('robot')
        player2 = Player('you  ', you_strategy)
    
    while cards:
        # print('\n\t\t', player1.name, player1.score)
        # print('\t\t\n', player2.name, player2.score)
        print(cards)
        cards = player1.play(cards)
        # print(cards)
        cards = player2.play(cards)

    print(cards2)
    print(player1.name, player1.score, player1.actions)
    print(player2.name, player2.score, player2.actions)


class Player:
    def __init__(self, name, strategy=strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0
        self.actions = []
    
    def play(self, cards):
        if len(cards) == 0:
            return cards
        action = self.strategy(cards)
        i = action if action == 0 else -1
        print('\t{} take {}'.format(self.name, cards[i]))
        if action == 0:
            self.score += cards[0]
            self.actions.append(cards[0])
            return cards[1:]
        else:
            self.score += cards[-1]
            self.actions.append(cards[1])
            return cards[:-1]

def you_strategy(cards):
    action = input('take which [head(0)/tail(1)]? ')
    return int(action)


def test_reconstruct_path():
    for _ in range(100):
        cards = gen_cards(60)
        T = max_min_iteratively(cards)
        path = reconstruct_path(cards, T)
        player1 = [action for (i,action) in enumerate(path) if i%2==0]
        player2 = [action for (i,action) in enumerate(path) if i%2==1]
        s1, s2 = 0, 0
        for i in range(len(player1)):
            a1, a2 = player1[i], player2[i]
            if a1 == 0:
                s1 += cards[0]
                cards = cards[1:]
            else:
                s1 += cards[-1]
                cards = cards[:-1]
            if a2 == 0:
                s2 += cards[0]
                cards = cards[1:]
            else:
                s2 += cards[-1]
                cards = cards[:-1] 
        assert T[0][-1] == (s1, s2)
    print('reconstruct_path test pass.')
        

if __name__ == '__main__':
    # test_reconstruct_path()
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        game(n)
    else:
        game()