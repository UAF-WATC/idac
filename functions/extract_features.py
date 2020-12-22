################################################
## ---- Extract Features From  Waveforms ---- ##
################################################

import idac as ida
import numpy as np
import obspy
import matplotlib.pyplot as plt
import os


def extract_features(wave_dir, save_dir, save_file, file_inds=[]):

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
    dme_features = inf.calc_features(dme_wig,dme_sps)

    ## setup an array to hold all the features
    all_features = np.zeros((len(wave_files),len(dme_features)))

    ## loop over synthetic event files
    i=0
    while i < len(wave_files):

        ## read in the current file
        cur_file_path = wave_dir + wave_files[i]
        cur_synth = obspy.read(cur_file_path)

        ## define the wiggle and sampling rate
        wig = cur_synth[0].data
        sps = cur_synth[0].stats.sampling_rate

        ########################
        ### EXTRACT FEATURES ###
        ########################

        ## calculate the current feature
        cur_features = inf.calc_features(wig, sps)

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




