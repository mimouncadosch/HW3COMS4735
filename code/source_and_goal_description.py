from spatial_rels import *
from spatial_rels import *
from transitivity import *

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

def source_and_goal_description(mbrs, S, G, T):
    # Return ids of buildings containing source and target points
    # Ids returned are indexed (1,28), similar to names
    s_id, g_id = (-1 for i in range(2))
    for i in range(len(mbrs)-2):
        if in_mbr(S, mbrs[i]) == True:
            s_id = i+1
        if in_mbr(G, mbrs[i]) == True:
            g_id = i+1

    names = get_building_names(mbrs, False)
    if s_id > -1:
        print "Source in " + names[s_id-1]
    if g_id > -1:
        print "Goal in " + names[g_id-1]

    return True