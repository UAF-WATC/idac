######################################
## ---- Calculate Overpressure ---- ##
######################################

import numpy as np


def calc_overpressure(weight, dist=1000, atm = 101325, src_type='nuclear'):

    '''
    weight = explosive yeild.  if chemical [Kg], if nuclear [Kilotons]
    dist = actual distance from explosion [m]
    atm = atmospheric pressure [Pa]
    src_type = whether to use nuclear or chemical equations

    returns overpressure in [Pa]
    '''

    ## calculate scaled distance
    z = dist/((2*weight)**(1/3)) ## [kim and rodgers 2016]
    z = dist/(weight**(1/3))

    #####################################
    ## calculate the overpressure [Pa] ##
    #####################################

    ## if nuclear
    if src_type == 'nuclear': 
        p_over = 3.2 * 10**6 * z**(-3) * (1 + (z/87)**2)**(1/2) * (1 + z/800) * atm
    #
    if src_type == 'chemical':
        p_over=(808*(1+(z/4.5)**2))/((1+(z/0.048)**2)**(1/2)*(1+(z/0.32)**2)**(1/2)*(1+(z/1.35)**2)**(1/2)) * atm
    #

    return(p_over)













