import cv2 as cv
import numpy as np
from description import *
from coordinate_extrema import *
from extrema import *

def main():
    img = cv.imread('../data/ass3-campus.pgm')
    labeled = cv.imread('../data/ass3-labeled.pgm')

    extrema = find_extrema(img, labeled)
    print "found extrema"
    # Iterate through each building to find descriptions
    for i in xrange(1, 28):
        # if i == 25:
            bld = np.uint8(labeled[:,:,0] == i) # Building mask. All three channels of labeled are equal

            # Return geometric features (centroid, area, area, upper left of MBR) and English description
            description(img, bld, i, extrema)

    return True


if __name__ == "__main__":
    main()

