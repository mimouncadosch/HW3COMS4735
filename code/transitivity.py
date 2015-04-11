import numpy as np
import cv2 as cv
import re
from spatial_rels import *

def transitivity(mbrs, img):

    T, M = create_matrix(mbrs)
    names = get_building_names()

    n = len(mbrs)
    # Loop through each source
    # for s in range(n):
    #     print_spatial_rels(s, names, T)

    return T, M

"""
Prints spatial relationships contained in matrix T
"""
def print_spatial_rels(source, names, T):
    n = T.shape[0]  # number of goals
    rels = ['North', 'South', 'East', 'West', 'Near']   # spatial relationships
    for p in range(5):
        # Don't print anything if there is are no relationships p for source building with other buildings
        if np.sum(T[:, source, p]) == 0:
            continue
        str = rels[p] + " of " + names[source] + " is: "
        for g in range(n):
            if T[g, source, p] == 1:
                str += names[g] + " , "
        print str
    return True

def get_building_names(): #, include_s_and_g
    names = []
    with open("../data/ass3-table.txt") as f:
        content = f.readlines()
        for i in range(len(content)):
            m = re.findall("\"(.+)\"", content[i])
            name = m[0]
            names.append(name)
    return names

def create_matrix(mbrs):
    n = len(mbrs)
    T = np.zeros((n,n,5))   # unfiltered matrix

    # TODO: Param P
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
                mbr_s = mbrs[s]
                mbr_g = mbrs[g]

                # Relevant points in building's MBR
                # S = xs, Xs, ys, Ys, ws, hs
                # G = xg, Xg, yg, Yg, wg, hg
                S = mbr_s[0], mbr_s[0]+mbr_s[2], mbr_s[1], mbr_s[1]+mbr_s[3], mbr_s[2], mbr_s[3]
                G = mbr_g[0], mbr_g[0]+mbr_g[2], mbr_g[1], mbr_g[1]+mbr_g[3], mbr_g[2], mbr_g[3]

                if p == 0:
                    T[g, s, p] = strict_north(S, G, P)
                if p == 1:
                    T[g, s, p] = strict_south(S, G, P)
                if p == 2:
                    T[g, s, p] = strict_east(S, G, P)
                if p == 3:
                    T[g, s, p] = strict_west(S, G, P)
                if p == 4:
                    T[g, s, p] = near(S, G)

    M = np.copy(T)   # matrix to be filtered
    filter_matrix(T, M)

    # Return unfiltered, filtered matrices
    return T, M

"""
Filter the matrix of size n x n
T is left unfiltered
M is matrix to be filtered
"""
def filter_matrix(T, M):
    m = M.shape[1]  # number of sources

    # Filter N, S, E, W relationships by transitivity
    for p in range(4):
        for f in range(m):
            filter_col_by_transitivity(T, M, f, p)

    # Filter "Near" relationships
    for f in range(m):
        filter_col_by_near(T, M, f)

    return True

"""
Filter each column of the matrix by transitivity
f is the index of the source building
p is the index relationship (0,1,2,3,4 for N,S,E,W,Near)
T is the unfiltered transitivity matrix
M is the filtered transitivity matrix
"""
def filter_col_by_transitivity(T, M, f, p):
    n = T.shape[0]
    for ri in range(n):
        for rj in range(n):
            # Indices must be indexed from (0,27)
            p_f_ri     = M[ri, f, p]
            p_ri_rj    = T[rj, ri, p]
            if p_f_ri == True and p_ri_rj == True:
                M[rj, f, p] = 0
    return True

"""
Filter each column of the matrix for "nearness"
f is the index of the source building
p is the index relationship (0,1,2,3,4 for N,S,E,W,Near)
T is the unfiltered transitivity matrix
M is the filtered transitivity matrix
"""
def filter_col_by_near(T, M, f):
    n = T.shape[0]
    for ri in range(n):
        for rj in range(n):
            near_ri_rj = T[rj, ri, 4]
            west_ri_rj = T[rj, ri, 3]
            east_ri_rj = T[rj, ri, 2]
            south_f_ri = M[ri, f, 1]
            north_f_ri = M[ri, f, 0]

            north_ri_rj = T[rj, ri, 0]
            south_ri_rj = T[rj, ri, 1]
            east_f_ri = M[ri, f, 2]
            west_f_ri = M[ri, f, 3]

            near_f_ri = M[ri,f, 4]

            if near_ri_rj and (west_ri_rj or east_ri_rj) and (south_f_ri or north_f_ri) and near_f_ri:
                M[rj, f, 4] = 0 # implied

            if near_ri_rj and (north_ri_rj or south_ri_rj) and (east_f_ri or west_f_ri) and near_f_ri:
                M[rj, f, 4] = 0 # implied

    return True