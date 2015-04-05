import cv2 as cv
import numpy as np
from description import *
from extrema import *
from spatial_rels import *
from time import sleep

S = (-1, -1)
G = (-1, -1)
clicks = 0

def main():
    global S
    global G
    mbrs = []

    img = cv.imread('../data/ass3-campus.pgm')
    labeled = cv.imread('../data/ass3-labeled.pgm')

    extrema = find_extrema(labeled)
    building_descriptions(img, labeled, extrema, mbrs)

    cv.namedWindow("image")
    cv.setMouseCallback("image", capture_position)

    # display the image and wait for a keypress
    cv.imshow("image", img)
    cv.waitKey(0) & 0xFF

    # Show source and goal points
    cv.circle(img, S, 1, (255,0,0),2)
    cv.circle(img, G, 1, (255,0,0),2)

    # cv.imshow("image", img)
    # cv.waitKey(0)

    spatial_relationships(labeled, S, G, img, mbrs)

    return True

def building_descriptions(img, labeled, extrema, mbrs):
    # Iterate through each building to find descriptions
    for i in xrange(1, 28):
        bld = np.uint8(labeled[:,:,0] == i) # Building mask. All three channels of labeled are equal
        # Return geometric features (centroid, area, area, upper left of MBR) and English description
        description(img, bld, i, extrema, mbrs)
    return True

def capture_position(event, x, y, flags, param):
    global S
    global G
    global clicks

    if event == cv.EVENT_LBUTTONDOWN:
        if clicks == 0:
            S = (x,y)
            print clicks, S
        if clicks == 1:
            G = (x,y)
            print clicks, G
            print "Please press any key to continue"

        clicks += 1
    return False


if __name__ == "__main__":
    main()

