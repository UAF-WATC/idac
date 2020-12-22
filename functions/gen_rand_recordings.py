##########################################
## ---- Generate Random Recordings ---- ##
##########################################


import idac as ida
import numpy as np
import obspy
import matplotlib.pyplot as plt
import os
from obspy.clients.fdsn import Client
import obspy
from obspy import UTCDateTime
import random


def gen_rand_recordings(client, network, station, location, channel, years, months, days, hours, mins, secs, n_wigs, save_dir):

    ## find all permutations of the inputs 
    all_inputs = [[i,j,k,l,m,n] for i in years for j in months for k in days for l in hours for m in mins for n in secs]

    ## define an index to sample all the inputs
    samp_inds = random.sample(range(1,len(all_inputs)), n_wigs)


    ## generate n_wigs worth of random times
    i=0
    while i < n_wigs:

        ## define the current inputs
        cur_inputs = all_inputs[samp_inds[i]]
        cur_inputs = [int(i) for i in cur_inputs]

        ## sample each of the time elements
        cur_year = cur_inputs[0]
        cur_month = cur_inputs[1]
        cur_day = cur_inputs[2]
        cur_hour = cur_inputs[3]
        cur_min = cur_inputs[4]
        cur_sec = cur_inputs[5]

        ## create a UTC time object
        cur_start=UTCDateTime(cur_year, cur_month, cur_day, cur_hour, cur_min, cur_sec)
        cur_stop = cur_start + 500

        ## read in the stream
        cur_stream = client.get_waveforms(network, station, location, channel, cur_start, cur_stop,attach_response=True)

        ## remove sensativity
        cur_stream.remove_sensitivity()

        ##############
        ### SAVING ###
        ##############

        ## get a good file name
        save_file = network + '_' + station + '_' + location + '_' + channel + '_' + str(cur_year) + '_' + str(cur_month) + '_' + str(cur_day) + '_' + str(cur_hour) + '_' + str(cur_min) + '_' + str(cur_sec) + '.mseed'

        save_path = save_dir + save_file

        cur_stream.write(save_path)

        i=i+1
        print(i)
    #

    return('done generating random recordings')





