import obspy
import idac as ida
import numpy as np
from scipy import signal    
from keras.models import load_model

import matplotlib.pyplot as plt


def deploy_ann_hrr(wig, model, sc, win_length, win_overlap):

    ## define the cur wiggles sampling rate
    sps = 1/np.median(np.diff(wig[:,0]))

    ## scipy filtering
    b, a = signal.butter(N=2, Wn=[0.02, 5], btype='bandpass',fs=sps)
    scipy_filter = signal.filtfilt(b, a, wig[:,1])

    ## save the filtered wiggle
    wig[:,1] = scipy_filter
    

    ######################################
    ### TURN WIGGLE INTO STREAM OBJECT ###
    ######################################
 
    ## turn the wiggle into a stream object
    eg_trace = obspy.Trace(wig[:,1])

    ## modify the trace statistics
    eg_trace.stats.sampling_rate = sps

    ## put the trace into a stream object
    eg_stream = obspy.Stream(eg_trace)
    
    ## resample the stream to match the training data
    eg_stream.resample(40)
    

    ######################
    ### ML PREDICTIONS ###
    ######################

    ## collect some features from this stream just to get the number of features
    dme_features = ida.calc_features(wig[:,1], sps)
    num_features = len(dme_features)

    ## Set up an empty array to hold all the features
    all_features = np.empty((len(wig[:,0]),num_features))
    all_features[:] = np.nan

    ## set up an empty array to hold all the feature times
    feature_times = np.empty(len(wig[:,0]))
    feature_times[:] = np.nan

    ## define the current start and stopping times
    cur_start = eg_stream[0].stats.starttime
    cur_stop = cur_start + win_length

    ## set up a counter to help populate all feature array
    j=0
    while cur_stop < eg_stream[0].stats.endtime:

        ## trim the trace
        cur_trace = eg_stream.copy()[0]
        cur_trace = cur_trace.trim(cur_start, cur_stop)


        ######################
        ## Extract Features ##
        ######################

        ##isolate the wiggle and sampling rate
        cur_win_wig = cur_trace.data
        sps = cur_trace.stats.sampling_rate

        ## normalize wiggle between 0 and 1 
        cur_win_wig = ida.range01(cur_win_wig)
        
        ## calculate the current features
        cur_features = ida.calc_features(cur_win_wig, sps)
        
        ## add the current features to the list for all windows
        all_features[j,:] = cur_features

        ## populate the feature times array
        cur_feature_time = (j)*win_length*(1-win_overlap) + (win_length/2) + wig[0,0]
        feature_times[j] = cur_feature_time

        ##move the start and end times
        cur_start = cur_start + win_length*(1-win_overlap)
        cur_stop = cur_start + win_length
        

        j=j+1
    #

    ## remove all the extra features and times
    ## would be nice to improve this if posisble
    all_features = all_features[0:j,:]
    feature_times = feature_times[0:j]

    ## reshape the feature times so that we may concat them to the predictions
    feature_times = feature_times.reshape(len(feature_times),1)
   
    ## scale the features
    all_features = sc.transform(all_features)
    
    ## make predictions
    all_preds = model.predict(all_features)

    ## isolate the probabilities of an event
    event_probs = all_preds[:,1].reshape(all_preds.shape[0],1)

    ## add the timing vector to the predictions
    all_times_preds = np.concatenate((feature_times, event_probs), axis=1)

    return(all_times_preds)
    

