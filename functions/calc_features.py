################################################
## ---- Calculate Features From Waveform ---- ##
################################################

import numpy as np
import obspy
import os
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import trigger_onset
from scipy.stats import kurtosis
from scipy.stats import skew


def calc_features(wig, sps, dmean = False):

    ## dmean if you want
    if dmean == True:
        wig = wig - np.mean(wig)
    #
    
    ## transform the wiggle to its absolute value
    wig_abs = np.abs(wig)
    

    #################
    ## Time Domain ## 
    #################

    ## mean
    td_mean = np.mean(wig_abs)

    ## standard deviation
    td_sd = np.std(wig)

    ## sum of skewness
    td_skew = skew(wig)

    ## sum of kurtosis
    td_kurt = kurtosis(wig)

    ## peak above mean (pam)
    pam = np.max(wig_abs - td_mean)

    ########################
    ## number of outliers ##
    ########################

    td_med = np.median(wig)
    td_q25 = np.quantile(wig,0.25)
    td_q75 = np.quantile(wig,0.75)
    inter_quantile = td_q75 - td_q25
    inner_range = inter_quantile * 1.5
    outer_range = inter_quantile * 3 

    ## find the fences
    inner_fences = [td_q25 - inner_range, td_q75 + inner_range]
    outer_fences = [td_q25 - outer_range, td_q75 + outer_range]

    td_lower_outliers = wig < outer_fences[0]
    td_upper_outliers = wig > outer_fences[1]
    td_outliers = np.where(td_lower_outliers + td_upper_outliers >= 1)

    ## number of outliers
    td_n_outliers = len(td_outliers[0])
    

    
    ######################
    ## event triggering ##
    ######################

    # ## create an obspy trace from the wiggle
    # wig_trace = obspy.Trace(wig)
    # wig_trace.stats.sampling_rate = sps

    # ## define a short and long term average
    # sta = 50
    # lta = 100

    # ## define a threshold
    # stalta_thresh = 1

    # ## generate a stalta series
    # stalta_series = classic_sta_lta(wig_trace.data, int(sta * sps), int(lta * sps))

    # ## find where the stalta series is above the threshold
    # triggers = trigger_onset(stalta_series,stalta_thresh,stalta_thresh)

    # ## how many triggers were there
    # td_num_triggers = len(triggers)

    # ##from obspy.signal.trigger import plot_trigger
    # ##plot_trigger(wig_trace, stalta_series, stalta_thresh, stalta_thresh)


    ######################
    ## Frequency Domain ##
    ######################

    ## how long is the trace
    n_wig = len(wig) / sps
    
    ## define the frequency step
    df = 1/n_wig

    ## frequency axis
    fax = np.arange(len(wig)) * df

    ## magnitude
    WIG = np.abs(np.fft.fft(wig))

    ## max frequency
    fd_max = np.max(WIG[0:int(len(WIG)/2)])

    ## find the peak frequency below the nyquist...
    fd_peak_freq = fax[np.argmax(WIG[0:int(len(WIG)/2)])]

    ## mean frequency
    fd_mean = np.mean(WIG)

    ## standard deviation
    fd_sd = np.std(WIG)

    ## skewness
    fd_skew = skew(WIG)

    ## kurtosis
    fd_kurt = kurtosis(WIG)

    ## quartiles
    all_quarts = np.quantile(WIG[0:int(len(WIG)/2)],[0.25, 0.5, 0.75])
    fd_25q = all_quarts[0]
    fd_50q = all_quarts[1]
    fd_75q = all_quarts[2]
    

    ### QUICK FD PLOTTING ##
    ##plt.plot(fax, WIG)
    ##plt.xlim(0,sps/2)
    

    ####################
    ## FEATURE SAVING ##
    ####################

    ##cur_features = [td_sd, td_mean, td_skew, td_kurt, pam, td_num_triggers, td_n_outliers, fd_max, fd_peak_freq, fd_mean, fd_sd, fd_skew, fd_kurt,fd_25q, fd_50q, fd_75q]
    cur_features = [td_sd, td_mean, td_skew, td_kurt, pam, td_n_outliers, fd_max, fd_peak_freq, fd_mean, fd_sd, fd_skew, fd_kurt,fd_25q, fd_50q, fd_75q]
   
    return(cur_features)


