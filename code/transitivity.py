import numpy as np
import cv2 as cv
import re
from spatial_rels import *

def transitivity(mbrs, img):

    T = create_matrix(mbrs)
    names = get_building_names(mbrs, True)

    n = len(mbrs)
    # Loop through each source
    for s in range(n):
        print_spatial_rels(s, names, T, mbrs)


    # cv.imshow("img", img)
    # cv.waitKey(0)
    return True

def print_spatial_rels(s, names, T, mbrs):
    n = len(mbrs)
    rels = ['North', 'South', 'East', 'West', 'Near']   # spatial relationships
    for p in range(5):
        if np.sum(T[:,s,p]) == 0:
            continue
        str = rels[p] + " of " + names[s] + " is: "
        for g in range(0,n):
            if T[g, s, p] == 1:
                str += names[g] + " , "

        print str
    return True

def get_building_names(mbrs, include_s_and_g):
    names = []
    with open("../data/ass3-table.txt") as f:
        content = f.readlines()
        for i in range(len(content)):
            m = re.findall("\"(.+)\"", content[i])
            name = m[0]
            names.append(name)

    if len(mbrs) > 27 and include_s_and_g == True:
        names.append("Source")
        names.append("Goal")

    return names


def get_name(id, names):

    return True

def create_matrix(mbrs):
    n = len(mbrs)
    T = np.zeros((n,n,5))
    P = 10

    # p = 0: north, 1: south, 2: east, 3: west, 4: near

    # Fill the transitivity matrix T
    # Iterate through each function (north, south, etc.)
    # range(27) => [0, 26] (27 buildings)
    for p in range(5):
        # Iterate through each building as source
        for s in range(n):
            # Iterate through each building as goal
            for g in range(n):
                if p == 0:
                    T[g, s, p] = strict_north(mbrs, s, g, P)
                if p == 1:
                    T[g, s, p] = strict_south(mbrs, s,g, P)
                if p == 2:
                    T[g, s, p] = strict_east(mbrs, s,g, P)
                if p == 3:
                    T[g, s, p] = strict_west(mbrs, s,g, P)
                if p == 4:
                    T[g, s, p] = near(mbrs, s,g)

    filter_matrix(T)

    return T

# Filter the matrix of size n x n
def filter_matrix(T):
    n = T.shape[0]
    # Filter N, S, E, W relationships by transitivity
    for p in range(4):
        for f in range(n):
            filter_col_by_transitivity(T, f, p)

    # Filter "Near" relationships
    for f in range(n):
        filter_col_by_near(T, f)

    return T

"""
Filter each column of the matrix by transitivity
f is the index of the source building
p is the index relationship (0,1,2,3,4 for N,S,E,W,Near)
T is the matrix
"""
def filter_col_by_transitivity(T, f, p):
    n = T.shape[0]
    for ri in range(n):
        for rj in range(n):
            # Indices must be indexed from (0,27)
            p_f_ri     = T[ri, f, p]
            p_ri_rj    = T[rj, ri, p]
            if p_f_ri == True and p_ri_rj == True:
                T[rj, f, p] = 0
    return True

"""
Filter each column of the matrix for "nearness"
f is the index of the source building
p is the index relationship (0,1,2,3,4 for N,S,E,W,Near)
T is the matrix
"""
def filter_col_by_near(T, f):
    n = T.shape[0]
    for ri in range(n):
        for rj in range(n):
            near_ri_rj = T[rj, ri, 4]
            west_ri_rj = T[rj, ri, 3]
            east_ri_rj = T[rj, ri, 2]
            south_f_ri = T[ri, f, 1]
            north_f_ri = T[ri, f, 0]

            north_ri_rj = T[rj, ri, 0]
            south_ri_rj = T[rj, ri, 1]
            east_f_ri = T[ri, f, 2]
            west_f_ri = T[ri, f, 3]

            near_f_ri = T[ri,f, 4]

            if near_ri_rj and (west_ri_rj or east_ri_rj) and (south_f_ri or north_f_ri) and near_f_ri:
                T[rj, f, 4] = 0 # implied

            if near_ri_rj and (north_ri_rj or south_ri_rj) and (east_f_ri or west_f_ri) and near_f_ri:
                T[rj, f, 4] = 0 # implied

    return True