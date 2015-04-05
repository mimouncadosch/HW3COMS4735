import numpy as np
import cv2 as cv
from max_perim_id import max_perim_id

def spatial_relationships(labeled, S, G, img, mbrs):

    # Get building ids
    s_id, g_id = get_bld_ids(mbrs, S, G)
    print s_id, g_id
    mbr_s = mbrs[s_id-1]
    mbr_g = mbrs[g_id-1]

    xs, ys, ws, hs = (mbr_s[i] for i in range(4))
    xg, yg, wg, hg = (mbr_g[i] for i in range(4))

    cv.rectangle(img, (xs, ys), (xs+ws, ys+hs), (255,0,100), 2)
    cv.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255,0,100), 2)
    cv.putText(img, "S", (S[0],S[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))
    cv.putText(img, "G", (G[0],G[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))

    # cv.imshow("image", img)

    print "img size", img.shape
    # print north(mbr_s, mbr_g)
    # print south(mbr_s, mbr_g)
    # print east(mbr_s, mbr_g)
    # print west(mbr_s, mbr_g)

    # cv.waitKey(0)

# Return ids of buildings containing source and target points
def get_bld_ids(mbrs, S, G):
    s_id, g_id = (-1 for i in range(2))
    for i in range(len(mbrs)):
        if in_mbr(S, mbrs[i]) == True:
            s_id = i+1
        if in_mbr(G, mbrs[i]) == True:
            g_id = i+1
    return s_id, g_id

def in_mbr(P, mbr):
    x,y,w,h = (mbr[i] for i in range(4))
    if P[0] <= (x+w) and P[1] <= (y+h) and P[0] >= x and P[1] >= y:
        return True
    return False

def north(mbr_s, mbr_g):
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]
    hg = mbr_g[3]

    dy = (ys - yg)
    if (hs+hg) <= dy:
        print "north"
        return True
    return False

def south(mbr_s, mbr_g):
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]
    hg = mbr_g[3]

    dy = (ys - yg)
    if hs+hg >= dy:
        print "south"
        return True
    return False

def east(mbr_s, mbr_g):
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    wg = mbr_g[2]

    dx = (xs - xg)
    if ws+wg  <= dx:
        print "east"
        return  True
    return False

def west(mbr_s, mbr_g):
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    wg = mbr_g[2]

    dx = (xs - xg)
    if ws+wg  >= dx:
        print "west"
        return  True
    return False


# def north(img, mbr_s, mbr_g):
#     yg = mbr_g[1]+mbr_g[3]
#     xg = mbr_g[0]
#     ys = mbr_s[1]
#     xs = mbr_s[0]
#     hs = mbr_s[3]
#     hg = mbr_g[3]
#     # PG = (xg, yg)
#     # PS = (xs, ys)
#     # clr = (255,0,255)
#     # cv.line(img, PG, PS, clr, 2)
#     # print ys - yg
#     # cv.imshow("img", img)
#     # cv.waitKey(0)
#
#     north = False
#     strict = False
#     # TODO: thresh
#     thresh = 50
#     a = ys - yg
#     if a >= 0:
#         north = True
#         strict = True
#     if a < 0 and a > -thresh:
#         north = True
#         strict = False
#     if a < -thresh:
#         north = False
#         strict = True
#
#     return {"north: ": north, "strict: ": strict}
#
#
# def south(img, mbr_s, mbr_g):
#     yg = mbr_g[1]
#     xg = mbr_g[0]
#     ys = mbr_s[1]+mbr_s[3]
#     xs = mbr_s[0]
#     hs = mbr_s[3]
#     hg = mbr_g[3]
#     # PG = (xg, yg)
#     # PS = (xs, ys)
#     # clr = (255,0,255)
#     # cv.line(img, PG, PS, clr, 2)
#     # cv.imshow("img", img)
#     # cv.waitKey(0)
#
#     south = False
#     strict = False
#     a = (yg - ys)
#     # TODO: thresh
#     thresh = 50
#     print a
#     if a >= 0:
#         south = True
#         strict = True
#     if a < 0 and a > -thresh:
#         south = True
#         strict = False
#     if a < -thresh:
#         south = False
#         strict = True
#
#     return  {"south: ": south, "strict: ": strict}
#
# def east(img, mbr_s, mbr_g):
#     yg = mbr_g[1]
#     xg = mbr_g[0]+mbr_g[2]
#     ys = mbr_s[1]
#     xs = mbr_s[0]
#     hs = mbr_s[3]
#     hg = mbr_g[3]
#     # PG = (xg, yg)
#     # PS = (xs, ys)
#     # clr = (255,0,255)
#     # cv.line(img, PG, PS, clr, 2)
#     # cv.imshow("img", img)
#     # cv.waitKey(0)
#     east = False
#     strict = True
#
#      # TODO: thresh
#     thresh = 50
#
#     a = xs - xg
#     if a >= 0:
#         east = True
#         strict = True
#     if a < 0 and a > -thresh:
#         east = True
#         strict = False
#     if a < -thresh:
#         east = False
#         strict = True
#
#     return {"east: ": east, "strict: ": strict}
#
# def west(img, mbr_s, mbr_g):
#     yg = mbr_g[1]
#     xg = mbr_g[0]
#     ys = mbr_s[1]
#     xs = mbr_s[0]+mbr_s[2]
#     hs = mbr_s[3]
#     hg = mbr_g[3]
#     # PG = (xg, yg)
#     # PS = (xs, ys)
#     # clr = (255,0,255)
#     # cv.line(img, PG, PS, clr, 2)
#     # cv.imshow("img", img)
#     # cv.waitKey(0)
#
#     a = xg - xs
#     # TODO: thresh
#     thresh = 50
#     west = False
#     strict = False
#     if a >= 0:
#         west = True
#         strict = True
#     if a < 0 and a > -thresh:
#         west = True
#         strict = False
#     if a < -thresh:
#         west = False
#         strict = True
#
#     return {"west: ": west, "strict: ": strict}

def near(S,G):
    return False

