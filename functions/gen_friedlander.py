##########################################################
## ---- Generate Friedlander Source Time Functions ---- ##
##########################################################
import os 
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import idac as ida

def gen_friedlander(weights, save_dir, time, dt, distances = [500], src_type='nuclear'):

    '''
    weights -- weight of the charge [KG]
    save_dir -- location where Friedlander waves will be saved
    time -- time length of the Friedlander blash wave [seconds]
    dt -- sampling frequency [seconds]
    distances -- distance from center of explosive charge to the target [m]
    src_type = whether to use nuclear or chemical equations
    '''

    ## generate at time axis
    tax = np.arange(time/dt) * dt
          
    ## loop over the weights
    i=0
    while i < len(weights):

        ## loop over the distances (normally this isn't needed)
        j=0
        while j < len(distances):

            ## grab the current weight and distance
            cur_weight = weights[i]
            cur_dist = distances[j]

            ## calculate the zero crossing crossing [seconds]
            cur_ts = ida.calc_zero_xing(cur_weight, cur_dist, src_type)

            ## calculate the the amplitude [Pa]
            cur_amp = ida.calc_overpressure(cur_weight, cur_dist, src_type=src_type)

            ## generate the Friedlander wave
            wig = cur_amp*np.exp(-tax/cur_ts) * (1 - tax/cur_ts)

            

            #################
            ### FILTERING ###
            #################

            from scipy.signal import butter, lfilter

            def butter_bandpass(highcut, fs, order):
                nyq = 0.5 * fs
                high = highcut / nyq
                b, a = butter(order, [high], btype='lowpass')
                return b, a


            def butter_bandpass_filter(data, highcut, fs, order):
                b, a = butter_bandpass(highcut, fs, order=order)
                y = lfilter(b, a, data)
                return y

            wig = butter_bandpass_filter(data=wig, highcut=1, fs=1/dt, order=4)

            #################




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



