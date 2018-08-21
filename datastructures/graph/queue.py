def makequeue(nodes):
    return sorted(nodes, key=lambda n: n.cost, reverse=True)

def deletemin(H):
    return H.pop()

def decreasekey(H, v):
    H.sort(key=lambda n: n.cost, reverse=True)