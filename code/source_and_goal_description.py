import numpy as np
from spatial_rels import *
from spatial_rels import *
from transitivity import *


def source_and_goal_description(mbrs, S, G, T):
    # Create tiny, "virtual" buildings for S and G pixels
    mbr_s, mbr_g = virtual_blds(mbrs, S, G)

    # Create an (n x 2) matrxi describing the unfiltered relationship between S,G and the rest of the buildings
    n = T.shape[0]  # number of goal buildings
    M = np.zeros((n, 2, 5))
    create_s_and_g_matrix(mbr_s, mbr_s, mbrs, T, M)

    # Return ids of buildings containing source and target points
    # Ids returned are indexed (1,28), similar to names
    s_id, g_id = get_bld_ids(mbrs, S, G)
    names = get_building_names(mbrs)
    if s_id > -1:
        print "Source in " + names[s_id-1]
    if g_id > -1:
        print "Goal in " + names[g_id-1]

    return True

def virtual_blds(mbrs, S, G):
    # This function creates two virtual buildings corresponding to the source and goal locations.
    # Our description of relative locations is based on building-pairs.
    # So it is necessary to treat the source and goal as buildings.
    # Buildings are represented by their MBR

    # TODO: param
    # Length and width of the width added to the MBR of the virtual building
    # Here the MBR is assumed to be a square
    l = 20
    # Virtual building upper right (x,y), width and height
    xs = S[0] - l/2
    ys = S[1] - l/2

    xg = G[0] - l/2
    yg = G[1] - l/2

    mbr_s = [xs, ys, l, l]
    mbr_g = [xg, yg, l, l]
    # mbrs.append([xs, ys, l, l])
    # mbrs.append([xg, yg, l, l])

    return mbr_s, mbr_g

    # return True


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