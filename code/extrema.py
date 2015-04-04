import numpy as np
import cv2 as cv
from max_perim_id import max_perim_id
def find_extrema(labeled):

    min_area = 10e3
    max_area = 0

    max_area_id = -1
    min_area_id = -1
    for i in xrange(1, 28):
        # Building mask. All three channels of labeled are equal
        bld = np.uint8(labeled[:,:,0] == i)
        # Building i contour
        contours, hierarchy = cv.findContours(bld, cv.RETR_TREE, cv.RETR_CCOMP, (0,0))
        # id of longest perimeter, length of longest perimeter.
        # Generally, there should be no more than one contour per building
        max_pid, max_p = max_perim_id(contours)

        area = cv.contourArea(contours[max_pid])

        # Update extreme values for different variables
        if area > max_area:
            max_area = area
            max_area_id = i
        if area < min_area:
            min_area = area
            min_area_id = i

    extrema = {"max_area":max_area, "min_area": min_area, "max_area_id":max_area_id, "min_area_id":min_area_id}

    return extrema
