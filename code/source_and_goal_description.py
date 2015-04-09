import numpy as np
from spatial_rels import *
from spatial_rels import *
from transitivity import *


def source_and_goal_description(mbrs, S, G, T, img):

    # Create an (n x 2) matrix describing the filtered relationship between S,G and the rest of the buildings
    M = create_s_and_g_matrix(S, G, mbrs, T)

    # Return ids of buildings containing source and target points
    # Ids returned are indexed (1,28), similar to names
    ids = get_bld_ids(mbrs, S, G)
    names = get_building_names(mbrs)
    print_spatial_rels_for_s_and_g(ids, names, M)

    equivalence_class(T, mbrs, img)

    return True

"""
Prints spatial relationships contained in matrix T
"""
def print_spatial_rels_for_s_and_g(ids, names, T):
    n = T.shape[0]  # number of goals
    rels = ['North', 'South', 'East', 'West', 'Near']   # spatial relationships
    extra_names = ["Source", "Goal"]

    for s in range(2):
        if ids[s] > -1:
            names.append(extra_names[s])
            for p in range(5):
                # Don't print anything if there is are no relationships p for source building with other buildings
                if np.sum(T[:, s, p]) == 0:
                    continue
                str = rels[p] + " of " + names[s+27] + " is: "
                for g in range(n):
                    if T[g, s, p] == 1:
                        str += names[g] + " , "
                print str
    return True

def equivalence_class(T, mbrs, img):
    # Create a matrix
    # M = np.meshgrid()
    # vec_strict_north = np.vectorize(strict_north)
    pupin = 0
    P = 10

    # vect_sn = np.vectorize(pixel_strict_north)
    # vect_sn(M, M, mbrs, lerner, P)

    # For each building:
    # for g in range(27):
    # for p in range(5):
    mbr_g = mbrs[11] # Low
    G = mbr_g[0], mbr_g[0]+mbr_g[2], mbr_g[1], mbr_g[1]+mbr_g[3], mbr_g[2], mbr_g[3]
    M = np.zeros((495,275), np.float32)
    N = np.zeros((495,275), np.float32)
    for c in range(495):
        for r in range(275):
            mbr_s = virtual_bld((r,c))
            S = mbr_s[0], mbr_s[0]+mbr_s[2], mbr_s[1], mbr_s[1]+mbr_s[3], mbr_s[2], mbr_s[3]
            # if p == 0:
            M[c,r] = strict_north(S, G, P)
            N[c,r] = strict_south(S, G, P)
            # print M[c,r]
                # if p == 1:
                #     M[c,r] = strict_south(S, G, P)
                # if p == 2:
                #     M[c,r] = strict_east(S, G, P)
                # if p == 3:
                #     M[c,r] = strict_west(S, G, P)
                # if p == 4:
                #     M[c,r] = near(S, G)
    M = M * 255
    N = N * 255
    # cv.imwrite("../images/M.jpg", M)
    cv.imwrite("../images/N.jpg", N)
                # print strict_south(S, G, P)


    return



# Strictly north calculation for pixels
def pixel_strict_north(xg, yg, mbrs, s_id, P):
    mbr_s = mbrs[s_id]
    ys = mbr_s[1]
    hs = mbr_s[3]
    xs = mbr_s[0]
    Xs = mbr_s[0]+mbr_s[2]

    # TODO: thresh
    # P = 30
    if ys >= yg + hs/2 and Xs > xg - P and xg + P > xs:
        return True
    return False

"""
This function creates a virtual building.
Our description of relative locations is based on building-pairs.
So it is necessary to treat the source and goal as buildings.
Buildings are represented by their MBR
"""
def virtual_bld(P):
    # TODO: param
    # Length and width of the width added to the MBR of the virtual building
    # Here the MBR is assumed to be a square
    l = 20
    # Virtual building upper right (x,y), width and height
    xs = P[0] - l/2
    ys = P[1] - l/2

    mbr = [xs, ys, l, l]

    return mbr

"""
"""
def create_s_and_g_matrix(S, G, mbrs, T):
    n = T.shape[0]  # number of goal buildings
    M = np.zeros((n, 2, 5)) # M contains the relationships for S and G with all other buildings
    # TODO: Param P
    P = 10

    # Create tiny, "virtual" buildings for S and G pixels
    mbr_s = virtual_bld(S)
    mbr_g = virtual_bld(G)
    virtual_blds = [mbr_s, mbr_g]

    for p in range(5):
        # Iterate through source
        for s in range(2):
            # Iterate through each building as goal
            for g in range(n):
                mbr_s = virtual_blds[s]
                mbr_g = mbrs[g]

                # S = xs, Xs, ys, Ys, ws, hs
                # G = xg, Xg, yg, Yg, wg, hg
                S = mbr_s[0], mbr_s[0]+mbr_s[2], mbr_s[1], mbr_s[1]+mbr_s[3], mbr_s[2], mbr_s[3]
                G = mbr_g[0], mbr_g[0]+mbr_g[2], mbr_g[1], mbr_g[1]+mbr_g[3], mbr_g[2], mbr_g[3]

                if p == 0:
                    M[g, s, p] = strict_north(S, G, P)
                if p == 1:
                    M[g, s, p] = strict_south(S, G, P)
                if p == 2:
                    M[g, s, p] = strict_east(S, G, P)
                if p == 3:
                    M[g, s, p] = strict_west(S, G, P)
                if p == 4:
                    M[g, s, p] = near(S, G)


    filter_matrix(T, M)

    return M