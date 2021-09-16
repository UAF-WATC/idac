import numpy as np
from scipy import signal    

def eval_ml_preds(det, pred):
    
    ##############
    ## RESAMPLE ## 
    ##############

    ## define the current predicted and detected sampling rate
    pred_sps = np.median(np.diff(pred[:,0]))
    det_sps = np.median(np.diff(det[:,0]))

    ## define the current time length
    cur_time = pred[-1,0] - pred[0,0]

    ## define how to resample
    resamp_f = 1 #[Hz]
    resamp_n = int(cur_time * resamp_f)
    
    ## resample
    pred_resamp = signal.resample(pred, resamp_n, axis=0, window=10)
    det_resamp = signal.resample(det, resamp_n, axis=0, window=10)
    
    ## create a time axis
    tax = np.arange(resamp_n) / resamp_f + pred_resamp[0,0]

    ## binarize (i.e. make predictions)
    cur_pred = pred_resamp[:,1] >= 0.5
    cur_det = det_resamp[:,1] >= 0.5


    ###############################
    ### CALCULATE TP, TN, ETC...###
    ###############################

    ## find all the event and non-event overlap indicies
    overlap_inds = np.where(cur_pred*1 + cur_det*1 == 2)
    overlap_non_event_inds = np.where(cur_pred*1 + cur_det*1 == 0)

    ## define how many detected events and non events there are
    num_det_events = len(np.where(cur_det == 1)[0])
    num_non_events = len(np.where(cur_det == 0)[0])

    cur_tp = len(overlap_inds[0])
    cur_tn = len(overlap_non_event_inds[0])
    cur_fn_fp = len(np.where(cur_pred*1 + cur_det*1 == 1)[0])

    cur_det_events = len(np.where(cur_det*1 == 1)[0])
    cur_det_non_events = len(np.where(cur_det*1 == 0)[0])

    ## put all these metrics in a list
    metrics = [cur_tp, cur_tn, cur_fn_fp, cur_det_events, cur_det_non_events]

    return(metrics)
#


