import random as r
class Deck(object):
    def __init__(self,N):
        self._deck = []
        for i in range(N):
            self._deck.append(i)

    def shuffle(self):
        for i in range(len(self._deck), 0, -1):
            k = r.randint(0,i)
            self._deck[i-1], self._deck[k] = self._deck[k], self._deck[i-1]
        return self._deck

d = Deck(10)
print d.shuffle()
