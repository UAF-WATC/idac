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
import idac as ida


# project_dir = '/home/alex/projects/idac_projects/final_run/propagation_projects/0_degrees/'
# rand_rec_dir =  project_dir + 'modeled_data/random_recordings/'
# prop_dir = project_dir + 'modeled_data/propagated_waves/'
# rem_shadow = False
# save_dir = project_dir + 'modeled_data/random_recordings/'
# snr_ratio = 1
# src_dir = project_dir + 'modeled_data/source_time_fxns/'


def add_noise2wave(rand_rec_dir, prop_dir, save_dir, snr_ratio=None):

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
        prop_wave_org = np.loadtxt(cur_prop_path)[:,1:3]

        ## make a copy of the original
        prop_wave = prop_wave_org.copy()

        ## sometimes there aren't any values in the propagated wave (rare)
        if any(np.isnan(prop_wave[:,1])):
            i=i+1
            continue
        #

        ###################################
        ## window the propagated arrival ##
        ###################################

        ## propagated wave sps 
        prop_wave_sps = 1/np.median(np.diff(prop_wave[:,0]))

        ## define arrival window length and samples
        arrival_win = 10 #seconds
        arrival_win_samps = arrival_win * prop_wave_sps

        ## find arrival of propagated wave
        arrival_ind = np.argmax(np.abs(prop_wave[:,1]))

        ## shift the arrival propagated wave so arrival is centered
        shift_by = (len(prop_wave) - arrival_ind) - int(len(prop_wave)/2)
        shift_prop_wave = prop_wave.copy()
        shift_prop_wave[:,1] = np.roll(shift_prop_wave[:,1], shift_by)

        ## finally window in the arrival
        shift_arrival_ind = np.argmax(np.abs(shift_prop_wave[:,1]))
        win_start = shift_arrival_ind - int(arrival_win_samps/2)
        win_end = shift_arrival_ind + int(arrival_win_samps/2)
        win_prop_wave = shift_prop_wave[win_start:win_end,:]
        

        ##################################################
        ## SCALE BACKGROUND NOISE BELOW PROPAGATED WAVE ##
        ##################################################

        ## stream sampling rate
        stream_sps = cur_stream[0].stats['sampling_rate']

        ## calculate power of stream and propagated wave
        stream_power = np.sum(np.abs(cur_stream[0].data)) / stream_sps / len(cur_stream[0].data)
        prop_wave_power = np.sum(np.abs(win_prop_wave[:,1])) / prop_wave_sps / len(win_prop_wave)

        ## current snr
        cur_snr = prop_wave_power / stream_power

        ## find the scale factor to force correct snr
        ## if no snr ratio is given
        if snr_ratio is None:
            scale_factor = 0
        #
        if snr_ratio is not None:
            scale_factor = 1/(stream_power * snr_ratio / prop_wave_power)
        #

        ## multiply the cur stream by the scale factor
        scale_stream = cur_stream.copy()
        scale_stream[0].data = scale_stream[0].data * scale_factor

        ## CHECK MODIFIED SNR RATIO ## 
        # t1 = np.sum(np.abs(scale_stream[0].data)) / stream_sps / len(cur_stream[0].data)
        # t2 = np.sum(np.abs(win_prop_wave[:,1])) / prop_wave_sps / len(win_prop_wave)  

        # ## current snr
        # t_snr = t2 / t1


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
        #synth_event = cur_stream[:]
        synth_event = scale_stream
        synth_event[0]=obspy.Trace(np.array(synth_event[0]) + prop_wave_resample[:,1])
        ##synth_event[0]=obspy.Trace(prop_wave_resample[:,1])

        synth_event[0].stats = cur_stream[0].stats

        ##############
        ### SAVING ###
        ##############

        save_file = cur_prop_file[:-4] + '.mseed'
        save_path = save_dir + save_file

        synth_event.write(save_path)
        ##synth_event.plot()

        i=i+1
        print(i)
    #

    return('done adding noise to waveform')






