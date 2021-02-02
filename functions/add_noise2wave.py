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



def add_noise2wave(rand_rec_dir, prop_dir, rem_shadow, save_dir, snr_ratio, src_dir):

    ##########################
    ### WHERE ARE THE DATA ###
    ##########################

    ## the random recordings
    rand_files = os.listdir(rand_rec_dir)

    ## the propagated waveform files
    prop_files = os.listdir(prop_dir)

    ## find the max amplitude for each source time function
    ## ro remove the shadow
    if rem_shadow == True:

        ## assume we know exactly where the source time functions are
        src_time_files = np.sort(os.listdir(src_dir))

        ## setup a list to hold the files and max amplitude
        src_amps = [np.nan] * len(src_time_files)

        ## loop over the source files
        i=0
        while i < len(src_time_files):

            ## what is the current source file
            cur_src_file = src_time_files[i]

            ## read in the current source function
            cur_src = np.loadtxt(src_dir + cur_src_file)

            ## find the max value in the current source
            cur_max = np.max(cur_src[:,1])

            ## populate the source amplitude list
            src_amps[i] = [cur_src_file, cur_max]
            i=i+1
        #
        
        
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


        ############################
        ### SHADOW ZONE ANALYSIS ###
        ############################

        ### CHECK IF PROPAGATED WAVE IS IN "SHADOW ZONE"
        if rem_shadow == True:

            ## grab meta data from propagated wave file
            prop_wave_info = cur_prop_file.split('_')

            ## what is the propagation distance
            prop_dist = float(prop_wave_info[7].split('.')[0]) * 1000 # [km] -> [m]

            ## find the source time functions
            source_time_fun_file = '_'.join(prop_wave_info[0:3]) + '.dat'

            ## find the maximum from the source amps list
            source_max = src_amps[np.where([source_time_fun_file in i for i in src_amps])[0][0]][1]

            ##source_time_fun = np.loadtxt(project_dir + 'modeled_data/source_time_fxns/' + source_time_fun_file)
            ## find the maximum of the source time function
            ##source_max = np.max(source_time_fun[:,1])


            ## define a shadow tolerance based on source amplitude and propagation distance
            shadow_tol = 1/prop_dist * source_max

            if np.max(prop_wave[:,1])*10 < shadow_tol:
                i=i+1
                print('pass')
                continue
        #


        #######################################
        ## SCALE WAVE ABOVE BACKGROUND NOISE ##
        #######################################

        ## define a minimum signal to noise ratio
        ##snr_ratio = 5  ## already defined in the input params file

        ## find noise in random recording
        mean_stream = np.mean(cur_stream[0][:])
        std_stream = np.std(cur_stream[0][:])
      
        ## scale propagated wave
        min_prop_wave = np.min(prop_wave_org[:,1])
        max_prop_wave = np.max(prop_wave_org[:,1] - min_prop_wave)

        prop_wave_scale = prop_wave.copy()
        prop_wave_scale[:,1] = ((prop_wave_org[:,1]-min_prop_wave)/max_prop_wave*2 -1)  * std_stream * snr_ratio

        ## move the scaled waveform back to the propagated wave name
        prop_wave = prop_wave_scale

        
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
        ##synth_event.plot()

        i=i+1
        print(i)
    #

    return('done adding noise to waveform')






