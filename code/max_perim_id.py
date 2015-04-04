# Find longest contour in image.
# In general, there should be only one contour per image
def max_perim_id(contours):
    max_perim_id = -1
    max_perim = -1
    for i in xrange(0,len(contours)):
        perim = cv.arcLength(contours[i], True)
        if(perim >= max_perim):
            max_perim = perim
            max_perim_id = i
    return max_perim_id, max_perim