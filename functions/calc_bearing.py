#################################
## ---- Calculate Heading ---- ##
#################################

import numpy as np
from  math import sin, cos, atan2, radians

def calc_bearing(p1, p2):

    lat1 = p1[0]
    long1 = p1[1]

    lat2 = p2[0]
    long2 = p2[1]


    ##y = math.sin(long2 - long1) * math.cos(lat2)
    ##x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1)

    x = cos(radians(lat2)) * sin(radians(long2 - long1))
    y = cos(radians(lat1))*sin(radians(lat2))-sin(radians(lat1))*cos(radians(lat2))*cos(radians(long2-long1))

    bearing = atan2(x,y) * 180/np.pi
    
    return(bearing)







