################################################
## ---- Run Infrasound Data Augmentation ---- ##
################################################

import idac as ida 

'''
## INPUTS ##
input_path -- input file containing all parameters needed to run the infrasound data augmentation workflow


## OUTPUTS ## 
multiple and potentially very large datafiles written to your local disk
'''


def run_ida(input_path, gen_atms=False, gen_friedlanders=False, gen_dispersion_curves=False, prop_waveforms=False,gen_rand_recordings=False, add_noise2waves=False) :

    ## read in (execute/open) the input file
    ns={}
    exec(open(input_path).read(), ns)

    ###########################
    ## BUILD THE ATMOSPHERES ##
    ###########################

    ## this generates files saved to a local directory
    if gen_atms == True: 
        ida.gen_atms(atm_build_dir=ns['atm_build_dir'], atm_save_dir=ns['atm_save_dir'], years=ns['atm_years'], months=ns['atm_months'], days=ns['atm_days'], hours=ns['atm_hours'], lats=ns['atm_lats'], longs=ns['atm_longs'], zmax=ns['zmax'], dz=ns['dz'])
    #

    
    ######################################################
    ### GENERATE THE FRIEDLANDER SOURCE TIME FUNCTIONS ###
    ######################################################

    ## this generates files saved to a local directory
    if gen_friedlanders == True: 
        ida.gen_friedlander(weights=ns['weights'], save_dir=ns['source_time_fun_save_dir'], time=ns['time'], dt=ns['dt'], src_type=ns['src_type'])
    #
    
    
    ##################################
    ### GENERATE DISPERSION CURVES ###
    ##################################

    ## this generates files saved to a local directory
    if gen_dispersion_curves == True: 
        ida.gen_dispersion_curves(atm_dir=ns['atm_save_dir'], dispersion_save_dir=ns['dispersion_save_dir'], f_min=ns['f_min'], f_step=ns['f_step'], f_max=ns['f_max'], prop_directions=ns['prop_directions'], disp_method=ns['disp_method'], which_cores=ns['which_cores'], wvnum_filter=ns['wvnum_filter'], c_min=ns['c_min'], c_max=ns['c_max'])
    #
    

    ##########################
    ### PROPAGATE WAVEFORM ###
    ##########################

    ## this generates files saved to a local directory
    if prop_waveforms == True:
        ida.prop_waveforms(dispersion_dir=ns['dispersion_save_dir'], source_time_fxn_dir=ns['source_time_fun_save_dir'], atm_dir=ns['atm_save_dir'], prop_dists=ns['prop_dists'], max_celerity=ns['max_celerity'], prop_wave_dir=ns['prop_wave_dir'])
    #
    

    ##################################
    ### GENERATE RANDOM RECORDINGS ###
    ##################################

    ## this generates files saved to a local directory
    if gen_rand_recordings == True:
        ida.gen_rand_recordings(ns['client'], ns['networks'], ns['stations'], ns['locations'], ns['channels'], ns['rand_years'], ns['rand_months'], ns['rand_days'], ns['rand_hours'], ns['rand_mins'], ns['rand_secs'], ns['n_rand_wigs'],ns['rand_save_dir'], wig_length=ns['rand_wig_length'])
    #
    

    ##################################
    ## ADD NOISE TO PROPAGATED WAVE ##
    ##################################

    ## this generates files saved to a local directory
    if add_noise2waves == True:
        ida.add_noise2wave(ns['rand_save_dir'], ns['prop_wave_dir'], ns['rem_shadow'], ns['noisy_wave_save_dir'], ns['snr_ratio'], ns['source_time_fun_save_dir'])
    #
    

    return()



