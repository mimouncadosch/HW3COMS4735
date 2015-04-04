import numpy as np
import cv2 as cv

def find_coordinate_extrema(img):
    mask = cv.inRange(img, (1,1,1), (255,255,255))
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.RETR_CCOMP)

    ctr_color = (0,100,100)
    nmost, smost, emost, wmost = ([] for i in range(4))

    # TODO: threshold
    t = 10
    img_h = img.shape[0]
    img_w = img.shape[1]

    # cv.line(img, (t, 0), (t,img_h), (0, 0, 250))
    # cv.line(img, (img_w-t, 0), (img_w-t,img_h), (0, 0, 250))
    # cv.line(img, (0, t), (img_w, t),(0, 0, 250))
    # cv.line(img, (0, img_h-t), (img_w, img_h-t), (0, 0, 250))

    for j in range(len(contours)):
        i = 27 - j
        print "i", i
        cv.drawContours(img, contours, i, (0,0,255), 2)
        cv.imshow("img", img)
        cv.waitKey(0)
    #     x,y,w,h = cv.boundingRect(contours[i])
    #     if x < t:
    #         emost.append(i+1)
    #     if (x+w) > (img_w - t):
    #         wmost.append(i+1)
    #     if (y+h) > (img_h-t):
    #         nmost.append(i+1)
    #     if (y) < t:
    #         smost.append(i+1)
    #
    # print nmost
    # print smost
    # print emost
    # print wmost

    return True

def old_find_coordinate_extrema(contours):
    x_max = 0
    y_max = 0
    x_min = 10e3
    y_min = 10e3
    n_most = []
    s_most = []
    e_most = []
    w_most = []

    # for i in range(len(contours)):
    #     cv.drawContours(campus, contours, i, (100,100,0),2)

    contour_vectors = []
    for i in range(len(contours)):
        num_pts = contours[i].shape[0]
        x, y = ([] for i in range(2))
        for j in range(0, num_pts*2,2):
            x.append(contours[i].flatten()[j])
        for k in range(1, num_pts*2,2):
            y.append(contours[i].flatten()[k])

        vector = np.matrix([x,y]).transpose()
        contour_vectors.append(vector)

        local_x_max = np.max(x)
        local_x_min = np.min(x)
        local_y_max = np.max(y)
        local_y_min = np.min(y)

        if local_x_max > x_max:
            x_max = local_x_max
        if local_y_max > y_max:
            y_max = local_y_max
        if local_x_min < x_min:
            x_min = local_x_min
        if local_y_min < y_min:
            y_min = local_y_min



    for i in range(len(contour_vectors)):
        n = np.where(contour_vectors[i] == y_max)
        if np.sum(n) > 0:
            n_most.append(i+1)
        s = np.where(contour_vectors[i] == y_min)
        if np.sum(s) > 0:
            s_most.append(i+1)
        e = np.where(contour_vectors[i] == x_min)
        if np.sum(e) > 0:
            e_most.append(i+1)
        w = np.where(contour_vectors[i] == x_max)
        if np.sum(w) > 0:
            w_most.append(i+1)

    return True