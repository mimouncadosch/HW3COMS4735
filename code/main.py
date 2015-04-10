import cv2 as cv
import numpy as np
from building_description import *
from extrema import *
from spatial_rels import *
from time import sleep
from transitivity import *
from source_and_goal_description import *

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
    #
    # # display the image and wait for a keypress
    cv.imshow("image", img)
    cv.waitKey(0) & 0xFF

    # Show source and goal points
    cv.circle(img, S, 1, (255,0,0),2)
    cv.circle(img, G, 1, (255,0,0),2)
    cv.imshow("image", img)
    cv.waitKey(0)

    # spatial_relationships(S, G, img, mbrs)

    # Unfiltered, filtered matrices
    T, M = transitivity(mbrs, img)
    source_and_goal_description(mbrs, S, G, T, img)
    # get_name(2)


    return True

def building_descriptions(img, labeled, extrema, mbrs):
    # Iterate through each building to find descriptions
    for i in range(1, 28):
        bld = np.uint8(labeled[:,:,0] == i) # Building mask. All three channels of labeled are equal
        # Return geometric features (centroid, area, area, upper left of MBR) and English description
        building_description(img, bld, i, extrema, mbrs)
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

