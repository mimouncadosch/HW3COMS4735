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

    # cv.rectangle(img, (xs, ys), (xs+ws, ys+hs), (255,0,100), 2)
    # cv.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255,0,100), 2)
    cv.putText(img, "S", (S[0],S[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))
    cv.putText(img, "G", (G[0],G[1]), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,100,200))

    # cv.imshow("image", img)

    print "img size", img.shape
    # print north(mbr_s, mbr_g)
    # print south(mbr_s, mbr_g)
    # print east(mbr_s, mbr_g)
    # print west(mbr_s, mbr_g)
    print near(img, mbr_s, mbr_g)

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

    if ys >= yg + hg:
        return True
    return False

def south(mbr_s, mbr_g):
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]
    hg = mbr_g[3]

    if yg >= ys + hs:
        return True
    return False

def east(mbr_s, mbr_g):
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    wg = mbr_g[2]

    if xs >= xg+wg:
        return True
    return False

def west(mbr_s, mbr_g):
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    wg = mbr_g[2]

    if xg >= xs+ws:
        return True
    return False

def near(img, mbr_s, mbr_g):
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

    cv.rectangle(img, (xs, ys), (xs+ws, ys+hs), (255,0,100), 2)
    cv.rectangle(img, (xg, yg), (xg+wg, yg+hg), (255,0,100), 2)
    cv.imshow("img", img)
    cv.waitKey(0)
    return near




    # print "Ws+Wg", Ws+Wg
    # print "Hs+Hg", Hs+Hg


