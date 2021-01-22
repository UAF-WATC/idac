#######################################
## ---- Calculate Zero Crossing ---- ##
#######################################


def calc_zero_xing(weight, dist=1000, src_type='nuclear'): 
    
    '''
    weight = explosive yeild.  if chemical [Kg], if nuclear [Kilotons]
    dist = actual distance from explosion [m]
    src_type = whether to use nuclear or chemical equations

    returns zero crossing in [seconds]
    '''

    ## calculate scaled distance
    ##z = dist/((2*weight)**(1/3)) ## [kim and rodgers 2016]
    z = dist/(weight**(1/3))

    
    #######################################
    ## calculate zero crossing [seconds] ##
    #######################################

    if src_type == 'nuclear': 
        zero_xing = (180*(1 + (z/100)**3)**(1/2)) / ((1 + z/40)**(1/2) * (1 +(z/285)**5)**(1/6) * (1+(z/50000))**(1/6)) * weight**(1/3) / 1000
    #

    if src_type == 'chemical':
        zero_xing = (980*(1+(z/0.54)**10))/((1+(z/0.02)**3)*(1+(z/0.74)**6)*(1+(z/6.9)**2)**(1/2))*weight**(1/3)

        ## remember to convert to seconds if chemical
        zero_xing = zero_xing / 1000

    return(zero_xing)





