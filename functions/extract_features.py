################################################
## ---- Extract Features From  Waveforms ---- ##
################################################

import idac as ida
import numpy as np
import obspy
import matplotlib.pyplot as plt
import os
from scipy import signal


def extract_features(wave_dir, save_dir, save_file, file_inds=[], filter_wig=False, scale_wig=False, win_wig=None):

    ##list all the waveform files
    wave_files = os.listdir(wave_dir)

    ## deterine which files to grab
    if len(file_inds) > 0:
        wave_files = list(np.array(wave_files)[file_inds])
    #
    

    ## read in one file to figure out how many features we will extract
    ##dme_prop = np.loadtxt(prop_dir + prop_files[0])
    dme_synth = obspy.read(wave_dir + wave_files[0])
    dme_wig = dme_synth[0].data
    dme_sps = dme_synth[0].stats.sampling_rate
    dme_features = ida.calc_features(dme_wig,dme_sps)

    ## setup an array to hold all the features
    all_features = np.zeros((len(wave_files),len(dme_features)))

    ## loop over synthetic event files
    i=0
    while i < len(wave_files):

        ## read in the current file
        cur_file = wave_files[i]
        cur_file_path = wave_dir + cur_file
        cur_synth = obspy.read(cur_file_path)

        ## define the wiggle and sampling rate
        wig = cur_synth[0].data
        sps = cur_synth[0].stats.sampling_rate

        ## filter
        if filter_wig==True:
            b, a = signal.butter(N=2, Wn=[0.01, 10], btype='bandpass',fs=sps)
            wig = signal.filtfilt(b, a, wig)
        #

        if scale_wig == True:
            wig = ida.scale_wig(wig)
        #

        ## window wiggle if necessary
        if win_wig is not None:

            ## pull out the info you need
            win = win_wig[0]
            shift_by= 0
            
            if len(win_wig) > 1:
                prop_dir = win_wig[1]

                ## grab the current prop file 
                cur_prop_file = cur_file[:-6] + '.dat'

                ## read in the current prop file
                cur_prop = np.loadtxt(prop_dir + cur_prop_file)

                ## find the time of the peak amplitude
                peak_amp_time = cur_prop[np.argmax(np.abs(cur_prop[:,2])),1] - np.min(cur_prop[:,1])

                ## find the index of this time on the synthetic event
                shift_by = np.argmin(np.abs(cur_synth[0].times() - peak_amp_time))
            #

            ## center the synthetic event based on the peak amplitude of the prpoagated wave
            wig_cent = wig.copy()
            wig_cent = ida.center_wig(wig, shift_by)

            ## now window the damn thing
            wig_start_ind = int(len(wig_cent)/2 - (win/2 * sps))
            wig_stop_ind = int(len(wig_cent)/2 + (win/2 * sps))
            windowed_wig = wig_cent[wig_start_ind:wig_stop_ind]

            ## save the centered wiggle
            wig = windowed_wig
        #
            

            
        
        ########################
        ### EXTRACT FEATURES ###
        ########################

        ## calculate the current feature
        cur_features = ida.calc_features(wig, sps)

        ## add the current feature to the all features array
        all_features[i,:] = cur_features

        i=i+1
        print(i)
    #


    ##############
    ### SAVING ###
    ##############

    save_path = save_dir + save_file
    np.savetxt(save_path, all_features)


    return('done extracting features')




