from spatial_rels import *

def virtual_blds(mbrs, S, G):
    # This function creates two virtual buildings corresponding to the source and goal locations.
    # Our description of relative locations is based on building-pairs,
    # so it is necessary to treat the source and goal as buildings.

    # TODO: param
    # Length and width of the width added to the MBR of the virtual building
    # Here the MBR is assumed to be a square
    l = 10
    # Virtual building upper right (x,y), width and height
    x = S[0]-l/2
    y = S[1] -l/2
    mbrs.append([x,y,l,l])

    return True

def source_and_goal_description(S, G, T):



    return True