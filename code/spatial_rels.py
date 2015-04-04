import numpy as np
import cv2 as cv
from max_perim_id import max_perim_id

def spatial_relationships(labeled, S, G):

    mbrs = []
    # Iterate through all buildings, compute their MBRs, and store them in mbr array
    for i in xrange(1, 28):
        bld = np.uint8(labeled[:,:,0] == i)
        contours, hierarchy = cv.findContours(bld, cv.RETR_TREE, cv.RETR_CCOMP, (0,0))
        max_pid, max_p = max_perim_id(contours)

        # Compute MBR
        x,y,w,h = cv.boundingRect(contours[max_pid])
        mbrs.append([x,y,w,h])

    for mbr in mbrs:
        print in_mbr(S, mbr)
        print in_mbr(G, mbr)

    return True


def in_mbr(P, mbr):
    x,y,w,h = (mbr[i] for i in range(4))

    if P[0] <= (x+w) and P[1] <= (y+h) and P[0] >= x and P[1] >= y
        return True

    return False


def north(S,G):
    return False


def south(S,G):
    return False


def east(S,G):
    return False

def west(S,G):
    return False

def near(S,G):
    return False

