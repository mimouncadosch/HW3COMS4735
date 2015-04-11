import numpy as np
import cv2 as cv
from collections import deque
import MyQueue

"""
M is filtered transitivity matrix
"""
def path_finding(M):


    b1 = 24   # id of building closest to source (B1)
    bn = 12  # id of building closest to goal (BN)

    n = M.shape[0]
    # Unified matrix: or product of all relationships of matrix M
    U = np.zeros((n, n))
    for p in range(5):
        # Matrix U represents the directed graph for all buildings in the image
        U = cv.bitwise_or(U, M[:,:,p])

    breadth_first_search(b1, bn, U)
    return True


def breadth_first_search(b1, bn, U):
    if b1 == bn:
        return True

    # previous = [None] * 10
    previous = []

    # Mark all buildings as not visited
    visited = [False] * n
    # visited = [False] * 8
    # Relations to building B1
    rels_b1 = U[:, b1]

    # Set relationship between building and itself to False
    rels_b1[b1] = False
    adjs_b1 = adjacent(rels_b1)

    # Create a queue for BFS
    q = MyQueue.MyQueue()

    # Mark current building as visited and enqueue it
    visited[b1] = True
    # Put first in array of adjacent in queue
    q.enqueue(b1)

    while not q.isEmpty():
        # Deque a building from the top of the queue and print it
        b = q.dequeue()
        print b
        # Get all adjacent buildings of the dequeued building b
        rels_b = U[:, b]
        rels_b[b] = False
        adjs = adjacent(rels_b)
        for i in range(len(adjs)):
            # If found destination building, stop
            curr = adjs[i]  # current node
            # if curr == bn:
            #     break
                # return True

            if visited[curr] == False:
                previous.append(b)
                visited[curr] = True
                q.enqueue(curr)

    return previous

"""
This function takes the 1 x n vector of relations for a given building b,
and returns a vector with the id's of the buildings that are adjacent to building b
"""
def adjacent(arr):
    adj = []    # vector of ids of adjacent buildings
    for i in range(len(arr)):
        if arr[i] == True:
            adj.append(i)

    return adj