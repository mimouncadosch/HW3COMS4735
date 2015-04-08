from spatial_rels import *

def virtual_blds(mbrs, S, G):
    # This function creates two virtual buildings corresponding to the source and goal locations.
    # Our description of relative locations is based on building-pairs,
    # so it is necessary to treat the source and goal as buildings.

    # TODO: param
    # Length and width of the width added to the MBR of the virtual building
    # Here the MBR is assumed to be a square
    l = 20
    # Virtual building upper right (x,y), width and height
    xs = S[0] - l/2
    ys = S[1] - l/2

    xg = G[0] - l/2
    yg = G[1] - l/2
    mbrs.append([xs, ys, l, l])
    mbrs.append([xg, yg, l, l])

    return True

def source_and_goal_description(S, G, T):



    return True