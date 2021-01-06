##########################################################
## ---- Generate Friedlander Source Time Functions ---- ##
##########################################################
import os 
import numpy as np
import matplotlib.pyplot as plt

def gen_friedlander(weights, save_dir, time, dt, scaled_distances = [1]):

    '''
    weights -- weight of the charge [KG]
    save_dir -- location where Friedlander waves will be saved
    time -- time length of the Friedlander blash wave [seconds]
    dt -- sampling frequency [seconds]
    distances -- distance from center of explosive charge to the target [m]
    '''

    ## generate at time axis
    tax = np.arange(time/dt) * dt
          
    ## loop over the weights
    i=0
    while i < len(weights):

        ## loop over the distances (normally this isn't needed)
        j=0
        while j < len(scaled_distances):

            ## grab the current weight and distance
            cur_weight = weights[i]
            cur_dist = scaled_distances[j]

            ## define the scaled distance
            cur_z = cur_dist/cur_weight

            ## calculate the zero crossing (ts) in milliseconds
            ## cur_ts_ms = (180*(1+(cur_z/100)**3)) / ( (1+(cur_z/40))**(1/2) * (1+(cur_z/285)**5)**(1/5) * (1+(cur_z/50000))**(1/6) )
            cur_ts_ms = (180*(1+(cur_z/100)**3)) / ( (1+(cur_z/40))**(1/2) * (1+(cur_z/285)**5)**(1/5) * (1+(cur_z/50000))**(1/6) ) * cur_weight**(1/3)
            

            ## put into seconds
            cur_ts = cur_ts_ms / 1000

            ## calculate the the amplitude
            cur_amp = 3.2 * 10**6 * cur_z**(-3) * (1+(cur_z/87)**2)**(1/2) * (1 + (cur_z/800))

            ## generate the Friedlander wave
            wig = cur_amp*np.exp(-tax/cur_ts) * (1 - tax/cur_ts)

            ## add the time axis and wiggle together
            fried_wave = np.zeros([len(tax),2])
            fried_wave[:,0] = tax
            fried_wave[:,1] = wig

            ## DME ##
            print(cur_ts, cur_amp)


            ############
            ## SAVING ##
            ############

            save_file = 'fried_' + str(cur_weight) + '_' +  str(cur_dist) + '.dat'
            np.savetxt(save_dir + save_file, fried_wave)

            j=j+1
        #
        i=i+1
    #
    return('done generating friedlander waves')



