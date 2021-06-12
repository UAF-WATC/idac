###################################
## ---- Scale Single Wiggle ---- ##
###################################
import numpy as np

def scale_wig(wig):
    
    scaled_wig = (wig - np.mean(wig)) / np.std(wig)

    return(scaled_wig)
#

