###################################################
## ---- Load in Atmosphere Data from AVOG2S ---- ##
###################################################

import numpy as np
import pandas as pd

def load_atm(path, meta=False):

    ## first read in the atmosphere data
    data = np.loadtxt(path)

    ## now grab the meta data if desired
    if meta == True:

        ## read the lines
        atm_file = open(path, 'r')

        ## read the lines of the file
        atm_lines = atm_file.readlines()

        ## get the metadata
        atm_metadata_all = [i for i in atm_lines if '#%' in i]
        atm_metadata = [i[3:] for i in atm_metadata_all if 'Z0' not in i]

        ## the variables and associated units
        atm_var = [i.split(',')[1] for i in atm_metadata]
        atm_units = [i.split(',')[2][:-1] for i in atm_metadata]

        ## make a pandas dataframe of metadata
        meta_df = pd.DataFrame([atm_var, atm_units])

        ## add the metadata to the
        return data, meta_df
    #
    else:
        return data
    #
#
