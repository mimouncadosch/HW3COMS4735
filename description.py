import cv2 as cv
from english_description import *

def description(img, mask):
    # Find geometric features and English descriptions of building: centroid, area, extrema of Minimum Bounding Rectangle,

    # (1) Geometric features
    # Find contours in the image
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE, (0,0))
    max_pid, max_p = max_perim_id(contours) # id of longest perimeter, length of longest perimeter

    # Parameter specifying the approximation accuracy.
    # This is the maximum distance between the original curve and its approximation.
    epsilon = 0.01 * max_p
    cv.approxPolyDP(contours[max_pid], epsilon, True)

    ctr_color = (0, 0, 255)
    cv.drawContours(img, contours, max_pid, ctr_color, 2, 8)

    area = cv.contourArea(contours[0])

    # Find image moments
    m = cv.moments(contours[max_pid])
    if m['m00'] > 0:
        cg = (int(m['m10']/m['m00']), int(m['m01']/m['m00']))
        cv.circle(img, cg, 2, (0, 0, 255), 2, 8)
    else:
        cg = (-1, -1)

    # Compute MBR
    x,y,w,h = cv.boundingRect(contours[max_pid])

    # Upper left, Bottom right of MBR
    ul = (x,y)
    br = (x+w, y+h)

    print "cg", cg
    print "area", area
    geom_features = {"area":area, "cg":cg, "ul":ul, "br":br}

    # Find English description of building
    english_description(geom_features)
    return geom_features



def english_description(geom_features):

    return True
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