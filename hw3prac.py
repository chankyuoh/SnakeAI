import time # provides time.sleep(0.5)
import random
import sys # larger recursive stack
from csplot import *
sys.setrecursionlimit(100000)  # 100,000 deep



def runGenerations( L ):
    """ runGenerations keeps running evolve...
    """
    if allOnes(L):
        print(L)
        return
    else:
        show(L)
        print(L)  # display the list, L
        time.sleep(0)  # pause a bit
        newL = evolve(L)  # evolve L into newL
        runGenerations(newL)  # recurse


def runGenerations2d( L ):
    """ runGenerations2d keeps running evolve in a 2D game of Lights-On
        input L: any list of integers in 2D format
    """
    if allOnes2d(L):
        show(L)
        print(L)
        return 0
    else:
        show(L)
        print(L) # display the list, L
        newL = evolve2d( L )  # evolve L into newL
        return 1 + runGenerations2d( newL ) # recurse

def evolve( L ):
    """ evolve takes in a list of integers, L,
    and returns a new list of integers
    considered to be the "next generation"
    """
    N = len(L)  # N now holds the size of the list L
    return [ setNewElement( L, i ) for i in range(N) ]


def setNewElement( L, i, x=0 ):
    """ setNewElement returns the NEW list's ith element
    input L: any list of integers
    input i: the index of the new element to return
    input x: an extra, optional input for future use
    """
    return random.choice([0,1])

def allOnes(L):
    for x in L:
        if x != 1:
            return False
    return True
runGenerations2d([[1,0,1],[0,1,1],[0,0,1]])