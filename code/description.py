from __future__ import division
import cv2 as cv
import numpy as np
from numpy import linalg as LA

def description(img, mask, id):
    # Find geometric features and English descriptions of building: centroid, area, extrema of Minimum Bounding Rectangle,

    # (1) Geometric features
    # Find contours in the image
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.RETR_CCOMP, (0,0))
    max_pid, max_p = max_perim_id(contours) # id of longest perimeter, length of longest perimeter

    # Epsilon: approx. accuracy. Max distance b/w original curve and approx.
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
    mbr = [x,y,w,h]

    # Upper left, Bottom right of MBR
    ul = (x,y)
    br = (x+w, y+h)
    geom_features = {"area":area, "cg":cg, "ul":ul, "br":br}

    cv.putText(img, str(id), (cg[0], cg[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,200, 0))
    cv.rectangle(img, (x,y), (x+w,y+h), (255,0,100), 2)

    # (2) Find English description of building
    # Each function gives the answer for a given description,
    # taking the necessary information from the shape
    # print has_hole(hierarchy)
    # print coord_orientation(x,y,w,h)
    # print symmetric(img, mbr, area)
    # img_shape = img.shape
    # coord_extrema(mbr, id, img_shape)

    # print northernmost(contours[max_pid], id)
    # letter_shape(img, contours[max_pid])
    # print orientation(m, img)
    cv.imshow("img", img)
    cv.waitKey(0)

    # print square_or_rectangular(w,h)

    return geom_features

# http://stackoverflow.com/questions/8461612/using-hierarchy-in-findcontours-in-opencv
def has_hole(hierarchy):
    for i in xrange(0, len(hierarchy[0])):
        if hierarchy[0][i][3] != -1:
            return True
    return False

def coord_orientation(x,y,w,h):
    # Use MBR
    # TODO: explain thresh
    thresh = 0.1

    r = float(h/w)
    ew, ns = (False for i in range(2))
    if r > (1+thresh):
        ns = True # oriented North-South
    elif r < (1-thresh):
        ew = True # oriented East-West

    return {"EW":ew, "NS":ns}

def symmetric(img, mbr, area):
    print "checking for symmetries"
    x,y,w,h = (mbr[i] for i in range(4))
    # Check for East-West symmetry
    bld = img[y:y+h, x:x+w]

    # Check for East-West symmetry
    img_one = img[y:(y+h), x:(x+w/2)]
    img_two = img[y:(y+h), x+w/2:x+w]

    if img_two.shape[1] > img_one.shape[1]: # Ensure matrices are same dimensions
        img_two = img[y:(y+h), x+w/2:x+w-1]
    img_two = cv.flip(img_two, 1)
    hor_diff = img_one - img_two

    # Number of nonzero pixels in horizontal difference matrix
    hor_non_zero = np.count_nonzero(hor_diff)

    # Check for North-South symmetry
    img_three = img[y:(y+h/2), x:x+w]
    img_four  = img[y+h/2:y+h, x:x+w]
    if img_four.shape[0] > img_three.shape[0]:  # Ensure matrices are same dimensions
        img_four = img[y+h/2:y+h-1, x:x+w]
    img_four = cv.flip(img_four, 0)
    ver_diff = img_three - img_four

    # Number of nonzero pixels in vertical difference matrix
    ver_non_zero = np.count_nonzero(ver_diff)

    # TODO: thresh and decision
    print "hor/area, ver/area", hor_non_zero/area, ver_non_zero/area
    thresh = 0.1
    ew, ns = (False for i in range(2))
    if hor_non_zero/area < thresh:
        ew = True
    if ver_non_zero/area < thresh:
        ns = True

    return {"EW":ew, "NS":ns}

def coord_extrema(mbr, id, img_shape):
    x,y,w,h = (mbr[i] for i in range(4))
    # TODO: threshold
    t = 10
    img_h = img_shape[0]
    img_w = img_shape[1]

    extrema = [0,0,0,0]
    if y < t:
        extrema[0] = 1
        print "northernmost"
    if (y+h) > (img_h-t):
        extrema[1] = 1
        print "southernmost"
    if x < t:
        extrema[2] = 1
        print "easternmost"
    if (x+w) > (img_w-t):
        extrema[3] = 1
        print "westernmost"

    return extrema

# Up to here tested & validated

def size(area):
    return True

def letter_shape(img, contour):
    if len(contour) >= 5:
        # Approx as ellipse and use axes
        ellipse = cv.fitEllipse(contour)
        cv.ellipse(img, ellipse, (0,100,100), 2, 8 )

        cv.imshow("img", img)
        cv.waitKey(0)

    return True

def orientation(m, img):
    if m['m00'] > 0:
        # Compute centroid using raw moments
        x_bar = int(m['m10']/m['m00'])
        y_bar = int(m['m01']/m['m00'])

        # Central moments of second order
        mu_00 = m['m00']
        mu_11 = m['m11'] - y_bar * m['m10']
        mu_20 = m['m20'] - x_bar * m['m10']
        mu_02 = m['m02'] - y_bar * m['m01']

        mu_p_20 = mu_20 / mu_00
        mu_p_02 = mu_02 / mu_00
        mu_p_11 = mu_11 / mu_00

        # Covariance matrix
        cov = np.matrix([[mu_p_20, mu_p_11],[mu_p_11, mu_p_02]])
        w, v = LA.eig(cov)
        vM = w[0]*v[:,0]/2     # major axis (axis of maximal intensity)
        vm = w[1]*v[:,1]/2   # minor axis (axis of minimal intensity)

        Mp1 = (x_bar - int(vM[0]/2), y_bar - int(vM[1]/2))
        Mp2 = (x_bar + int(vM[0]/2), y_bar + int(vM[1]/2))
        # p1 = (Mp1, Mp2)

        mp1 = (x_bar - int(vm[0]/2), y_bar - int(vm[1]/2))
        mp2 = (x_bar + int(vm[0]/2), y_bar + int(vm[1]/2))
        # p2 = (mp1, mp2)
        cv.line(img, Mp1, Mp2, (0, 100, 0))
        cv.line(img, mp1, mp2, (0, 100, 0))

        print w,v
        cv.imshow("img", img)
        cv.waitKey(0)
    return True

def square_or_rectangular(w,h):
    # TODO: explain thresh
    thresh = 0.1 # Threshold for the ratio w/h for a shape to be considered square vs. rectangular
    if ( w/h < (1+thresh) ) or ( w/h > (1-thresh) ):
        return 'sq'
    return 'rect'

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