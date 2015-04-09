import numpy as np
from spatial_rels import *
from spatial_rels import *
from transitivity import *


def source_and_goal_description(mbrs, S, G, T):
    # Create tiny, "virtual" buildings for S and G pixels
    mbr_s = virtual_bld(S)
    mbr_g = virtual_bld(G)

    # Create an (n x 2) matrxi describing the unfiltered relationship between S,G and the rest of the buildings
    n = T.shape[0]  # number of goal buildings
    M = np.zeros((n, 2, 5))

    # M is the matrix we wish to filter, using the relationships in M
    create_s_and_g_matrix(mbr_s, mbr_g, mbrs, T, M)

    # Return ids of buildings containing source and target points
    # Ids returned are indexed (1,28), similar to names
    s_id, g_id = get_bld_ids(mbrs, S, G)
    names = get_building_names(mbrs)
    # if s_id > -1:
    #     print "Source in " + names[s_id-1]
    #     names.append("Source")
    #     print_spatial_rels_for_s_and_g(0, names, M)
    # if g_id > -1:
    #     print "Goal in " + names[g_id-1]
    #     names.append("Goal")
    #     print_spatial_rels_for_s_and_g(1, names, M)

    # TODO: PRINT Relationshiops to S, G

    # equivalence_class(T, mbrs)

    return True

"""
Prints spatial relationships contained in matrix T

"""
def print_spatial_rels_for_s_and_g(source, names, T):
    n = T.shape[0]  # number of goals
    rels = ['North', 'South', 'East', 'West', 'Near']   # spatial relationships
    for p in range(5):
        # Don't print anything if there is are no relationships p for source building with other buildings
        if np.sum(T[:, source, p]) == 0:
            continue
        str = rels[p] + " of " + names[source+27] + " is: "
        for g in range(n):
            if T[g, source, p] == 1:
                str += names[g] + " , "
        print str
    return True

def equivalence_class(T, mbrs):
    # Create a matrix
    M = np.meshgrid()
    vec_strict_north = np.vectorize(strict_north)
    lerner = 24
    P = 10

    vect_sn = np.vectorize(pixel_strict_north)
    vect_sn(M, M, mbrs, lerner, P)

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


def virtual_bld(P):
    # This function creates a virtual building.
    # Our description of relative locations is based on building-pairs.
    # So it is necessary to treat the source and goal as buildings.
    # Buildings are represented by their MBR

    # TODO: param
    # Length and width of the width added to the MBR of the virtual building
    # Here the MBR is assumed to be a square
    l = 20
    # Virtual building upper right (x,y), width and height
    xs = P[0] - l/2
    ys = P[1] - l/2

    mbr = [xs, ys, l, l]

    return mbr

def create_s_and_g_matrix(mbr_s, mbr_g, mbrs, T, M):
    n = M.shape[0]
    # TODO: Param P
    P = 10

    for p in range(5):
        # Iterate through source and goal
        for s in range(2):
            # Iterate through each building as goal
            for g in range(n):
                if p == 0:
                    M[g, s, p] = strict_north(mbrs, s, g, P)
                if p == 1:
                    M[g, s, p] = strict_south(mbrs, s,g, P)
                if p == 2:
                    M[g, s, p] = strict_east(mbrs, s,g, P)
                if p == 3:
                    M[g, s, p] = strict_west(mbrs, s,g, P)
                if p == 4:
                    M[g, s, p] = near(mbrs, s,g)

    filter_matrix(T, M)

    return True