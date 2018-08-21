class DisjointSet:
    def __init__(self, x):
        self.item = x
        self.parent = self
        self.rank = 0
    
    def find(self):
        x = self
        while x is not x.parent:
            x = x.parent
        return x
    
    def union(self, us):
        x = self.find()
        y = us.find()
        if x is y:
            return
        if x.rank > y.rank:
            y.parent = x
        elif x.rank < y.rank:
            x.parent = y
        else:
            x.parent = y
            y.rank += 1

    
def test():
    us = DisjointSet(1)
    assert us.find() == us
    us2 = DisjointSet(2)
    us.union(us2)
    assert us.find() == us2
    us3 = DisjointSet(3)
    us3.union(us)
    assert us3.find() == us2
    print('DisjointSet tests pass.')


if __name__ == '__main__':
    test()