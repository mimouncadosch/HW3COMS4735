import numpy as np
from spatial_rels import *
from spatial_rels import *
from transitivity import *

"""
T is unfiltered relationship matrix
"""
def source_and_goal_description(mbrs, S, G, T, img):

    # Create an (n x 2) matrix describing the filtered relationship between S,G and the rest of the buildings
    F = create_s_and_g_matrix(S, G, mbrs, T)

    # Return ids of buildings containing source and target points
    # Ids returned are indexed (1,28), similar to names
    ids = get_bld_ids(mbrs, S, G)
    names = get_building_names(mbrs)
    print_spatial_rels_for_s_and_g(ids, names, F)

    P = 40
    # create_equivalence_classes(mbrs, P)

    draw_point_clouds(F, P)

    return True


def draw_point_clouds(M, P):

    # Buildings related to S and their relation to S
    blds_s = []
    rels =  ['N', 'S', 'E', 'W', "Ne"]

    I = np.ones((495, 275), np.uint8)

    # Do it for source first
    # For each relationship
    for p in range(5):
        # # For each source building
        # for s in range(2):
            # For each goal building
            for g in range(27):
                if M[g, 0, p] == True: # s instead of 0
                    # J = np.ones((495, 275), np.float32)
                    J = cv.imread("../images/" + str(P) + "/" + str(rels[p]) + "_" + str(g) + ".png",0)
                    I = cv.bitwise_and(I, J)
                    # I = I * 255
                    # cv.imshow("I", I)
                    # cv.waitKey(0)

    I = I * 255
    cv.imshow("FINAL", I)
    cv.waitKey(0)
    return True


"""
Prints spatial relationships contained in matrix T
"""
def print_spatial_rels_for_s_and_g(ids, names, T):
    n = T.shape[0]  # number of goals
    rels = ['North', 'South', 'East', 'West', 'Near']   # spatial relationships
    # rels = ['South', 'North', 'West', 'East', 'Near']   # spatial relationships
    extra_names = ["Source", "Goal"]
    print ids
    for s in range(2):
        if ids[s] > -1:
            names.append(extra_names[s])
            for p in range(5):
                # Don't print anything if there is are no relationships p for source building with other buildings
                if np.sum(T[:, s, p]) == 0:
                    continue
                # str = names[s+27] + " is " + rels[p] + " of "
                str = rels[p] + " of " + names[s+27] + " is: "
                for g in range(n):
                    if T[g, s, p] == 1:
                        str += names[g] + " , "
                print str
    return True

def create_equivalence_classes(mbrs, P):
    # Create a matrix

    for s in range(27):
        N = np.zeros((495,275), np.float32)
        South = np.zeros((495,275), np.float32)
        E = np.zeros((495,275), np.float32)
        W = np.zeros((495,275), np.float32)
        NE = np.zeros((495,275), np.float32)
        for c in range(495):
            for r in range(275):
                mbr_s = mbrs[s]
                S = mbr_s[0], mbr_s[0]+mbr_s[2], mbr_s[1], mbr_s[1]+mbr_s[3], mbr_s[2], mbr_s[3]
                mbr_g = virtual_bld((r,c))
                G = mbr_g[0], mbr_g[0]+mbr_g[2], mbr_g[1], mbr_g[1]+mbr_g[3], mbr_g[2], mbr_g[3]

                N[c,r] = strict_north(S, G, P)
                South[c,r] = strict_south(S, G, P)
                E[c,r] = strict_east(S, G, P)
                W[c,r] = strict_west(S, G, P)
                NE[c,r] = near(S, G)

        N = N * 255
        South = South * 255
        E = E * 255
        W = W * 255
        NE = NE * 255
        cv.imwrite("../images/" + str(P) + "/S_" + str(s) + ".png", N)
        cv.imwrite("../images/" + str(P) + "/N_" + str(s) + ".png", South)
        cv.imwrite("../images/" + str(P) + "/W_" + str(s) + ".png", E)
        cv.imwrite("../images/" + str(P) + "/E_" + str(s) + ".png", W)
        cv.imwrite("../images/" + str(P) + "/Ne_" + str(s) + ".png", NE)

    return True



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
def create_s_and_g_matrix(S, G, mbrs, M):
    n = M.shape[0]  # number of goal buildings
    F = np.zeros((n, 2, 5)) # M contains the relationships for S and G with all other buildings
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
                    F[g, s, p] = strict_north(S, G, P)
                if p == 1:
                    F[g, s, p] = strict_south(S, G, P)
                if p == 2:
                    F[g, s, p] = strict_east(S, G, P)
                if p == 3:
                    F[g, s, p] = strict_west(S, G, P)
                if p == 4:
                    F[g, s, p] = near(S, G)


    filter_matrix(M, F)

    return F