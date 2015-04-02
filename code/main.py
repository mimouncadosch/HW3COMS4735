import cv2 as cv
import numpy as np
from description import *

def main():
    campus = cv.imread('../data/ass3-campus.pgm')
    labeled = cv.imread('../data/ass3-labeled.pgm')

    # cv.imshow("normalized img", campus_img)
    # cv.waitKey(0)

    # Iterate through each building to find descriptions
    for i in xrange(1, 28):
        bld = np.uint8(labeled[:,:,0] == i) # all three channels of labeled are equal

        # Return geometric features (centroid, area, area, upper left of MBR)

        description(campus, bld)




    return True


if __name__ == "__main__":
    main()

