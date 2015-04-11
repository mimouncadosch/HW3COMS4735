import numpy as np
import cv2 as cv
from collections import deque
import MyQueue
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from transitivity import get_building_names
"""
T is unfiltered transitivity matrix
M is filtered transitivity matrix
"""
def path_finding(T, M):


    b1 = 0   # id of building closest to source (B1)
    # bn = 2
    bn = 25  # id of building closest to goal (BN)

    n = M.shape[0]
    # Unified matrix: or product of all relationships of matrix M
    U = np.zeros((n, n))
    for p in range(5):
        # Matrix U represents the directed graph for all buildings in the image
        U = cv.bitwise_or(U, M[:,:,p])

    # plot_graph(U)
    # U = np.zeros((8,8))
    # U[1,0] = 1
    # U[3,0] = 1
    # U[6,0] = 1
    #
    # U[0,1] = 1
    # U[4,1] = 1
    # U[5,1] = 1
    #
    # U[5,2] = 1
    # U[7,2] = 1
    #
    # U[0,3] = 1
    # U[5,3] = 1
    #
    # U[1,4] = 1
    # U[6,4] = 1
    #
    # U[1,5] = 1
    # U[2,5] = 1
    # U[3,5] = 1
    #
    # U[0,6] = 1
    # U[4,6] = 1
    #
    # U[2,7] = 1
    dir_array, bfs_array = breadth_first_search(b1, bn, U)

    # print bfs_array

    names = get_building_names()
    # print dir_array

    # print filtered_array
    for i in range(len(dir_array)):
        print names[dir_array[i]]
    # print_directions(dir_array, M)
    return True


# def filter_dir_array(dir_array, U):
#     s = dir_array[0]
#     filtered_dir_array = [s]
#
#     for g in range(len(dir_array)):
#         if U[g, s] == True:
#             continue
#         elif U[g, s] == False:
#             filtered_dir_array.append(dir_array[g])
#
#     return filtered_dir_array

def plot_graph(U, names):
    G = nx.from_numpy_matrix(U)

    # label
    # pos=nx.spring_layout(G) # positions for all nodes
    #
    # nx.draw_networkx_labels(G,pos,labels,font_size=16)
    #
    # nx.draw(G)
    #
    # plt.show()
    # TODO: Change back to MACOSX format /usr/local/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
    # G=nx.cubical_graph()
    pos=nx.spring_layout(G) # positions for all nodes
    #
    # nodes
    nx.draw_networkx_nodes(G,pos,
                           nodelist=range(13),
                           node_color='r',
                           node_size=500,
                       alpha=0.8)
    nx.draw_networkx_nodes(G,pos,
                           nodelist=range(13,26),
                           node_color='b',
                           node_size=500,
                       alpha=0.8)

    # # edges
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
    # nx.draw_networkx_edges(G,pos,
    #                        edgelist=[(0,1),(1,2),(2,3),(3,0)],
    #                        width=8,alpha=0.5,edge_color='r')
    # nx.draw_networkx_edges(G,pos,
    #                        edgelist=[(4,5),(5,6),(6,7),(7,4)],
    #                        width=8,alpha=0.5,edge_color='b')


    # some math labels
    labels={}

    for i in range(len(names)):
        labels[i] = names[i]
    nx.draw_networkx_labels(G,pos,labels,font_size=16)

    plt.axis('off')
    plt.show() # display
    # plt.savefig("labels_and_colors.png") # save as png

    return True

def print_directions(dir_array, M):
    print len(dir_array)
    for i in range(len(dir_array)-1):
        print_direction(dir_array[i], dir_array[i+1], M)

    return True

def print_direction(s_id, g_id, M):
    coords = ["north", "south", "east", "west", "near"]
    dir = "Go to the building that is "
    for p in range(5):
        if M[g_id, s_id, p] == True:
            dir += str(coords[p]) + " , "

    print dir
    # dir += " (which is "
    # description(g_id)

    return True

def breadth_first_search(b1, bn, U):
    n = U.shape[0]
    if b1 == bn:
        return True

    previous = [None] * n
    # previous = []
    bfs = []

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
        bfs.append(b)
        # Get all adjacent buildings of the dequeued building b
        rels_b = U[:, b]
        rels_b[b] = False
        adjs = adjacent(rels_b)
        for i in range(len(adjs)):
            # If found destination building, stop
            curr = adjs[i]  # current node

            if visited[curr] == False:
                # print "previous["+str(curr)+"]="+str(b)
                previous[curr] = b
                visited[curr] = True
                q.enqueue(curr)

    path = unique(previous, bn, b1)
    return path, bfs

"""
dest
origin
"""
def unique(arr, dest, origin):
    found = False
    path = []
    init = arr.index(dest)
    # Init must be index of origin, not whatever it is now.
    j = init
    while not found:
        k = arr[j]
        path.append(k)
        if k == origin:
            break
        j = k

    return path


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