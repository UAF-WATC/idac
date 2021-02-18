##########################################
## ---- Load Source Time Functions ---- ##
##########################################

import os
import numpy as np

def load_src_fxns(path, return_meta=False):

    ## list the source function files
    src_fxn_files = np.sort(os.listdir(path))

    ## set up a list to the hold the metadata
    src_metadata = ['']*len(src_fxn_files)
    
    ## read in the source time functions via a loop
    i=0
    while i < len(src_fxn_files):

        ## current src path
        cur_src_path = path + src_fxn_files[i]

        ## read in the current source
        cur_src = np.loadtxt(cur_src_path)

        ## if first iteration initilize an array to hold everything
        if i==0:
            all_srcs = np.zeros((len(cur_src), len(src_fxn_files)+1))

            ## add the time to the first column of the array
            all_srcs[:,0] = cur_src[:,0]
        #

        ## populate the src array with the current source wiggle
        all_srcs[:,(i+1)] = cur_src[:,1]

        ## grab some metadata
        src_metadata[i] = src_fxn_files[i]
        

        i=i+1
    #
    if return_meta == True:
        return(all_srcs, src_metadata)
    if return_meta == False:
        return(all_srcs)
    #
#

    



