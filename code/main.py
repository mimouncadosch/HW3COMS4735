import cv2 as cv
import numpy as np
from description import *
from coordinate_extrema import *

def main():
    img = cv.imread('../data/ass3-campus.pgm')
    labeled = cv.imread('../data/ass3-labeled.pgm')

    # Iterate through each building to find descriptions
    for i in xrange(1, 28):
        # if i == 25:
            bld = np.uint8(labeled[:,:,0] == i) # all three channels of labeled are equal

            # Return geometric features (centroid, area, area, upper left of MBR)
            description(img, bld, i)

    return True

    # find_coordinate_extrema(img, contours)

if __name__ == "__main__":
    main()

