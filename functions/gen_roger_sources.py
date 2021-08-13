####################################################
## ---- Generate Roger Source Time Functions ---- ##
####################################################

import idac as ida
import obspy
import numpy as np
import scipy
import os


# project_dir = '/home/alex/projects/idac_projects/final_run/propagation_projects/0_degrees/'
# save_dir = project_dir + 'modeled_data/source_time_fxns/'
# data_dir = '/home/alex/projects/idac_projects/hrr/data/hrr_raw/hrr5_hrr6/'
# min_scale_dist=20
# max_scale_dist=50
# yields = {'HRR-1':18140, 'HRR-2':18140, 'HRR-3':9070, 'HRR-4':9070, 'HRR-5':45360, 'HRR-6':45270}
# f_min=0.1
# f_max=1
# source_length=100
 
##def gen_roger_sources(data_dir, save_dir, yields, f_min, f_max, min_scale_dist=20, max_scale_dist=50, source_length=100, sps_resample=40):
def gen_roger_sources(data_dir, save_dir, yields, f_max, min_scale_dist=20, max_scale_dist=50, source_length=100, sps_resample=40):

    '''
    data_dir -- location of near source recorded data
    save_dir -- where the source time functions will be saved
    f_min -- float, lower corner of filter, [Hz]
    f_max -- float, upper corner of filter, [Hz]
    min_scale_dist -- float, minimum scaled distance considered [km]
    max_scale_dist -- float, maximum scaled distance considered [km]
    source_length -- float, length of source time function [secs]
    yields -- dict, names of explosions (e.g. HRR-5) and associated yield (e.g. 45360)
    sps_resample -- float, desired sampling rate of source time function.  
    '''

    ## list all the datafiles
    data_files = os.listdir(data_dir)

    ## loop over the datafiles
    i=0
    while i < len(data_files):

        ## cur datafiles
        cur_datafile = data_files[i]

        ## read in the current datafiles as a obspy trace object
        cur_trace = obspy.read(data_dir + cur_datafile)[0]

        ## what is the current explosion
        cur_explosion = cur_datafile.split('_')[0]

        ## grab the yield associated with the current trace
        cur_yield = yields[cur_explosion]

        ## what is the current source to receiver distance
        cur_dist = cur_trace.stats['sac']['dist']

        ## what is the current scaled source to receiver distance
        cur_scaled_dist = cur_dist*1000 / cur_yield**(1/3)
       
        ## only proceed if this trace is from the near field 
        if cur_scaled_dist < min_scale_dist or cur_scaled_dist > max_scale_dist:
            i=i+1
            continue
        #

        ##################
        ## DOWNSAMPLING ##
        ##################

        ## define resampling sample rate
        ##sps_resample = 80##40 # [sps] ## defined in function
        cur_trace.resample(sps_resample)
        

        #################
        ### FILTERING ###
        #################

        cur_trace.detrend(type='constant')
        ##cur_trace.filter('bandpass', freqmin=f_min, freqmax=f_max, corners=2, zerophase=True)
        cur_trace.filter('lowpass', freq=f_max, corners=2, zerophase=True)
        cur_trace.taper(max_percentage=.01)

        
        ## what is the current samples per second
        cur_sps = cur_trace.stats.sampling_rate

        ## fit a roger wave to the current data wiggle
        cur_roger = ida.fit_roger2data(cur_trace, cur_sps)

        ## check if there was a fit
        if any(np.isnan(cur_roger)):
            i = i+1
            continue
        #
            

        #############
        ## SCALING ## 
        #############

        ## max amplitude of current trace
        cur_max_amp = np.max(cur_trace.data)

        ## find scaling factor
        scale_factor = cur_dist * 1000

        ## scale Roger's wave
        scaled_roger_wave = cur_roger * cur_dist * 1000 / 1 * 2 
        print(np.round(cur_dist), np.round(cur_scaled_dist), np.round(np.max(scaled_roger_wave)))


        ##########
        ## TRIM ##
        ##########

        ## create a time axis
        tax = np.arange(len(cur_roger)) / cur_sps + 1/cur_sps

        ## combine tax and scaled rogers wave into array
        roger_array_all = np.array([tax, scaled_roger_wave]).T

        ## trim the roger array according to the time length
        keep_inds = int(source_length * cur_sps)
        roger_array = roger_array_all[0:keep_inds,:]
        
        ######################
        ### QUICK PLOTTING ###
        ######################
        # import matplotlib.pyplot as plt
        # plt.close('all')
        # plt.ion()

        # td_pad_left=3
        # td_pad_right=7
        
        # import matplotlib.pyplot as plt

        # ## shift the rogers cur stream
        # shift_by = np.argmax(cur_trace.data) - np.argmax(cur_roger)
        # plot_roger_wig = np.roll(cur_roger, shift_by)

        # fig, axs = plt.subplots(1,2)
        # axs[0].plot(tax, cur_trace.data, label='HRR5 Data', linewidth=5)
        # axs[0].plot(tax, plot_roger_wig, label='Fitted Roger Wave')

        # axs[0].set_xlim(tax[shift_by]-td_pad_left, tax[shift_by]+td_pad_right)
        # axs[0].legend()
        # axs[0].set_xlabel('time [secs]')

        # axs[1].plot(tax, scaled_roger_wave)
        # axs[1].set_xlim(-1, 8)
        # plt.ginput(1)
      

        ############
        ## SAVING ##
        ############

        save_file = cur_datafile[:-3] + 'dat'
        save_path = save_dir + save_file
        np.savetxt(save_path, roger_array)
        

        i=i+1
    #
#





