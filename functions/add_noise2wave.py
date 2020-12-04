##########################################
## ---- Add Noise to Propated Wave ---- ##
##########################################
 
import numpy as np
import os
import matplotlib.pyplot as plt
import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import scipy.signal as signal


def add_noise2wave(rand_rec_dir, prop_dir, amp_scale, rem_shadow, save_dir):

    ##########################
    ### WHERE ARE THE DATA ###
    ##########################

    ## the random recordings
    rand_files = os.listdir(rand_rec_dir)

    ## the propagated waveform files
    prop_files = os.listdir(prop_dir)

    ## loop over the propagated files
    i=0
    while i < len(prop_files):

        #######################
        ### READ IN THE DATA ##
        #######################

        ## the current random recording
        cur_rand_file = rand_files[i]
        cur_rand_path = rand_rec_dir + cur_rand_file

        ## read in the stream
        cur_stream = obspy.read(cur_rand_path)

        ## the propagated data
        cur_prop_file = prop_files[i]
        cur_prop_path = prop_dir + cur_prop_file

        ## read in the propagated wave
        prop_wave_org = np.loadtxt(cur_prop_path)

        ## scale the propagated wave
        prop_wave = prop_wave_org[:]
        prop_wave[:,1] = prop_wave_org[:,1] * amp_scale

        ### CHECK IF PROPAGATED WAVE IS IN "SHADOW ZONE"
        if rem_shadow == True:
            shadow_tol = 2 #[Pa]
            if np.max(prop_wave[:,1]) < shadow_tol:
                i=i+1
                print('pass')
                continue
        #


        ###################################################
        ### ADD RANDOM RECORDED DATA TO PROPAGATED WAVE ###
        ###################################################

        ## how many points are in inf_wig
        n_wig = len(cur_stream[0])

        ### resample propagated wave to match infrasound wiggle
        prop_wave_resample = np.zeros([n_wig,2])
        prop_wave_resample[:,0] = np.linspace(prop_wave[0,0],prop_wave[-1,0], n_wig)
        prop_wave_resample[:,1] = signal.resample(prop_wave[:,1], n_wig)

        ## add the resampled propagated wave to the infrasound wiggle
        synth_event = cur_stream[:]
        synth_event[0]=obspy.Trace(np.array(synth_event[0]) + prop_wave_resample[:,1])

        synth_event[0].stats = cur_stream[0].stats

        ##############
        ### SAVING ###
        ##############

        save_file = cur_prop_file[:-4] + '.mseed'
        save_path = save_dir + save_file


        synth_event.write(save_path)

        i=i+1
        print(i)
    #

    return('done adding noise to waveform')






