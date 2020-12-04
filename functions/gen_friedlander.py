##########################################################
## ---- Generate Friedlander Source Time Functions ---- ##
##########################################################
import os 
import numpy as np
import matplotlib.pyplot as plt

def gen_friedlander(save_dir, amps, tss, time, dt): 

    ## loop over the amplitudes
    i=0
    while i < len(amps):

        ## loop over the zero crossings
        j=0
        while j < len(tss):

            ## grab the current amplitude and zero crossing
            cur_amp = amps[i]
            cur_ts = tss[j]

            ## generate the time axis and wiggle
            tax = np.arange(time/dt) * dt
            wig = cur_amp*np.exp(-tax/cur_ts) * (1 - tax/cur_ts)

            ## add the time axis and wiggle together
            fried_wave = np.zeros([len(tax),2])
            fried_wave[:,0] = tax
            fried_wave[:,1] = wig


            ############
            ## SAVING ##
            ############

            save_file = 'fried_' + str(cur_amp) + '_' +  str(cur_ts) + '.dat'
            np.savetxt(save_dir + save_file, fried_wave)

            j=j+1
        #
        i=i+1
    #
    return('done generating friedlander waves')



