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

def near(img, mbr_s, mbr_g):
    xs = mbr_s[0]
    xg = mbr_g[0]
    ws = mbr_s[2]
    wg = mbr_g[2]
    ys = mbr_s[1]
    yg = mbr_g[1]
    hs = mbr_s[3]
    hg = mbr_g[3]

    dx = abs(xs - xg)
    dy = abs(ys - yg)
    print "dx", dx
    print "dy", dy

    p = 0.01
    # Enlarged MBRs
    Ws = int(ws+p*hs)
    Hs = int(hs+p*ws)

    Wg = int(wg+p*hg)
    Hg = int(hg+p*wg)

    cv.rectangle(img, (xs, ys), (xs+Ws, ys+Hs), (255,0,100), 2)
    cv.rectangle(img, (xg, yg), (xg+Wg, yg+Hg), (255,0,100), 2)

    print "Ws+Wg", Ws+Wg
    print "Hs+Hg", Hs+Hg
    cv.imshow("enlarged", img)
    cv.waitKey(0)


    if dx <= (Ws + Wg) and dy <= (Hs+Hg):
        return True

    return False

