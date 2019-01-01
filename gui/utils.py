from collections import deque
from requests import get

def downloadList(url="https://www.minorplanetcenter.net/iau/NEO/neocp.txt"):
    return get(url).text

class PriorityQue(deque):
    def uplift(self, i):
        """i - index, if last element it remains there"""
        if i+1 != len(self):
            target = self[i]
            move = self[i+1]
            self[i] = move
            self[i+1] = target

    def downlift(self, i):
        """i - index, if first element it remains there"""
        if i != 0:
            target = self[i]
            move = self[i-1]
            self[i] = move
            self[i-1] = target



class MinorPlanet:
    def __init__(self, name, ra, de, v):
        """
        MPC object information container
        name - [string]
        ra - right ascension
        de - declination
        v - magnitude
        """
        self.name = name
        self.ra = ra
        self.de = de
        self.v = v

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
