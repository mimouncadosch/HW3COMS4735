import numpy as np
import cv2 as cv
import re
from spatial_rels import *

def transitivity(mbrs, img):

    T = create_matrix(mbrs)
    names = get_building_names()

    for s in range(27):
        name = names[s]
        for p in range(5):
            if p == 0:
                str ="North of " + name + " is "
                for g in range(0,27):
                    if T[g,s,p] == 1:
                        str += names[g] + ","
            if p == 1:
                str = "South of " + name + " is "
                for g in range(0,27):
                    if T[g,s,p] == 1:
                        str += names[g] + ", "
            if p == 2:
                str = "East of " + name + " is "
                for g in range(0,27):
                    if T[g,s,p] == 1:
                        str += names[g] + ", "

            if p == 3:
                str = "West of " + name + " is "
                for g in range(0,27):
                    if T[g,s,p] == 1:
                        str += names[g] + ", "

            if p == 4:
                str = "Near " + name + " is "
                for g in range(0,27):
                    if T[g,s,p] == 1:
                        str += names[g] + ", "
            print str
        print "\n"

    cv.imshow("img", img)
    cv.waitKey(0)
    return True


def get_building_names():
    names = []
    with open("../data/ass3-table.txt") as f:
        content = f.readlines()
        for i in range(len(content)):
            m = re.findall("\"(.+)\"", content[i])
            name = m[0]
            names.append(name)
    return names


def get_name(id, names):



    return True

def create_matrix(mbrs):
    T = np.zeros((27,27,5))

    # p = 0: north, 1: south, 2: east, 3: west, 4: near

    # Fill the transitivity matrix T
    # Iterate through each function (north, south, etc.)
    # range(27) => [0, 26] (27 buildings)
    for p in range(5):
        # Iterate through each building as source
        for s in range(27):
            # Iterate through each building as goal
            for g in range(27):
                if p == 0:
                    T[g, s, p] = strict_north(mbrs, s, g)
                if p == 1:
                    T[g, s, p] = strict_south(mbrs, s,g)
                if p == 2:
                    T[g, s, p] = strict_east(mbrs, s,g)
                if p == 3:
                    T[g, s, p] = strict_west(mbrs, s,g)
                if p == 4:
                    T[g, s, p] = near(mbrs, s,g)

    # Filter N, S, E, W relationships by transitivity
    for p in range(4):
        for f in range(27):
            for ri in range(27):
                for rj in range(27):
                    # Indices must be indexed from (0,27)
                    p_f_ri     = T[ri, f, p]
                    p_ri_rj    = T[rj, ri, p]
                    if p_f_ri == True and p_ri_rj == True:
                        T[rj, f, p] = 0

    # Filter "Near" relationships
    for f in range(27):
        for ri in range(27):
            for rj in range(27):
                near_ri_rj = T[rj, ri, 4]
                west_ri_rj = T[rj, ri, 3]
                east_ri_rj = T[rj, ri, 2]
                south_f_ri = T[ri, f, 1]
                north_f_ri = T[ri, f, 0]

                north_ri_rj = T[rj, ri, 0]
                south_ri_rj = T[rj, ri, 1]
                east_f_ri = T[ri, f, 2]
                west_f_ri = T[ri, f, 3]

                near_f_ri = T[ri,f, 4]

                if f == 11 and ri == 12 and rj == 8:
                    print "here"
                if near_ri_rj and (west_ri_rj or east_ri_rj) and (south_f_ri or north_f_ri) and near_f_ri:
                    T[rj, f, 4] = 0 # implied


                if near_ri_rj and (north_ri_rj or south_ri_rj) and (east_f_ri or west_f_ri) and near_f_ri:
                    T[rj, f, 4] = 0 # implied

    return T