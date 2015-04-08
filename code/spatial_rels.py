import numpy as np
import cv2 as cv
from max_perim_id import max_perim_id

def spatial_relationships(labeled, S, G, img, mbrs):

    # Get building ids
    s_id, g_id = get_bld_ids(mbrs, S, G)
    print s_id, g_id
    mbr_s = mbrs[s_id-1]
    mbr_g = mbrs[g_id-1]

    # xs, ys, ws, hs = (mbr_s[i] for i in range(4))
    # xg, yg, wg, hg = (mbr_g[i] for i in range(4))
    # cv.rectangle(img, (xs, ys), (xs+ws, ys+hs), (255,0,100), 2)
    # cv.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255,0,100), 2)
    # cv.putText(img, "S", (S[0],S[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))
    # cv.putText(img, "G", (G[0],G[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))

    # cv.imshow("image", img)

    # print "img size", img.shape
    # print strict_north(mbrs, s_id-1, g_id-1, 10)
    # print near(mbrs, s_id-1, g_id-1)

    # cv.waitKey(0)

# Return ids of buildings containing source and target points
# Ids returned are indexed (1,28), similar to names
def get_bld_ids(mbrs, S, G):
    s_id, g_id = (-1 for i in range(2))
    for i in range(len(mbrs)):
        if in_mbr(S, mbrs[i]) == True:
            s_id = i+1
        if in_mbr(G, mbrs[i]) == True:
            g_id = i+1
    return s_id, g_id

# Returns true if points P is inside the MBR
def in_mbr(P, mbr):
    x,y,w,h = (mbr[i] for i in range(4))
    if P[0] <= (x+w) and P[1] <= (y+h) and P[0] >= x and P[1] >= y:
        return True
    return False

# For north, south, east, west, near:
# mbrs: array of minimum bounding rectangles
# s: id of source building (indexed 0-26)
# g: id of goal building (indexed 0-26)
def north(mbrs, s_id, g_id):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    ys = mbr_s[1]
    yg = mbr_g[1]
    hg = mbr_g[3]

    if ys >= yg + hg/2:
        return True
    return False

def strict_north(mbrs, s_id, g_id, P):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    ys = mbr_s[1]
    yg = mbr_g[1]
    hg = mbr_g[3]
    xs = mbr_s[0]
    Xs = mbr_s[0]+mbr_s[2]
    xg = mbr_g[0]
    Xg = mbr_g[0]+mbr_g[2]

    # TODO: thresh
    # P = 30
    if ys >= yg + hg/2 and Xs > xg - P and Xg + P > xs:
        return True
    return False

def south(mbrs, s_id, g_id):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]

    if yg >= ys + hs/2:
        return True
    return False

def strict_south(mbrs, s_id, g_id, P):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]
    xs = mbr_s[0]
    Xs = mbr_s[0]+mbr_s[2]
    xg = mbr_g[0]
    Xg = mbr_g[0]+mbr_g[2]

    # TODO: thresh
    # P = 30
    if yg >= ys + hs/2 and Xs > xg - P and Xg + P > xs:
        return True
    return False

def east(mbrs, s_id, g_id):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    xs = mbr_s[0]
    xg = mbr_g[0]
    wg = mbr_g[2]

    if xs >= xg + wg/2:
        return True
    return False

def strict_east(mbrs, s_id, g_id, P):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    xs = mbr_s[0]
    xg = mbr_g[0]
    wg = mbr_g[2]
    ys = mbr_s[1]
    Ys = mbr_s[1]+mbr_s[3]
    yg = mbr_g[1]
    Yg = mbr_g[1]+mbr_g[3]

    # TODO: thresh
    # P = 30
    if xs >= xg + wg/2 and Ys > yg - P and Yg + P > ys:
        return True
    return False

def west(mbrs, s_id, g_id):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]

    if xg >= xs + ws/2:
        return True
    return False


def strict_west(mbrs, s_id, g_id, P):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    ys = mbr_s[1]
    Ys = mbr_s[1]+mbr_s[3]
    yg = mbr_g[1]
    Yg = mbr_g[1]+mbr_g[3]

    # TODO: thresh
    # P = 30
    if xg >= xs + ws/2 and Ys > yg - P and Yg + P > ys:
        return True
    return False

def near(mbrs, s_id, g_id):
    mbr_s = mbrs[s_id]
    mbr_g = mbrs[g_id]
    xs = mbr_s[0]
    xg = mbr_g[0]
    Xs = mbr_s[0]+mbr_s[2]
    Xg = mbr_g[0]+mbr_g[2]
    ws = mbr_s[2]
    wg = mbr_g[2]
    ys = mbr_s[1]
    yg = mbr_g[1]
    Ys = mbr_s[1]+mbr_s[3]
    Yg = mbr_g[1]+mbr_g[3]
    hs = mbr_s[3]
    hg = mbr_g[3]

    # TODO: thresh
    p = 1.5
    # Find if horizontally close
    hor_close = False
    if xs < Xg:
        dx = Xg - xs
    elif Xg < Xs:
        dx = Xs - xg

    if dx <= p*(ws+wg):
        hor_close = True

    # Find if vertically close
    ver_close = False
    if ys < Yg:
        dy = Yg - ys
    elif Yg < Ys:
        dy = Ys - yg

    if dy <= p*(hs+hg):
        ver_close = True


    near = hor_close and ver_close

    return near

