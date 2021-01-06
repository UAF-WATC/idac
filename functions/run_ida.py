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


#input_path = '/home/alex/projects/idac_projects/test/input_parameters/eg1_input_params.py'


def run_ida(input_path) :

    ## read in (execute/open) the input file
    exec(open(input_path).read())

    ###########################
    ## BUILD THE ATMOSPHERES ##
    ###########################

    ## this generates files saved to a local directory
    ida.gen_atms(atm_build_dir=atm_build_dir, atm_save_dir=atm_save_dir, years=atm_years, months=atm_months, days=atm_days, hours=atm_hours, lats=atm_lats, longs=atm_lats, zmax=zmax, dz=dz)

    
    ######################################################
    ### GENERATE THE FRIEDLANDER SOURCE TIME FUNCTIONS ###
    ######################################################

    ## this generates files saved to a local directory
    ida.gen_friedlander(weights=weights, save_dir=source_time_fun_save_dir, time=time, dt=dt)

    
    ##################################
    ### GENERATE DISPERSION CURVES ###
    ##################################

    ## this generates files saved to a local directory
    ida.gen_dispersion_curves(atm_dir=atm_save_dir, dispersion_save_dir=dispersion_save_dir, f_min=f_min, f_step=f_step, f_max=f_max, prop_directions=prop_directions)
    

    ##########################
    ### PROPAGATE WAVEFORM ###
    ##########################

    ## this generates files saved to a local directory
    ida.prop_waveforms(dispersion_dir=dispersion_save_dir, source_time_fxn_dir=source_time_fun_save_dir, atm_dir=atm_save_dir, prop_dists=prop_dists, max_celerity=max_celerity, prop_wave_dir=prop_wave_dir)


    ##################################
    ### GENERATE RANDOM RECORDINGS ###
    ##################################

    ## this generates files saved to a local directory
    ida.gen_rand_recordings(client, network, station, location, channel, years, months, days, hours, mins, secs, n_wigs,rand_save_dir)


    ##################################
    ## ADD NOISE TO PROPAGATED WAVE ##
    ##################################

    ## this generates files saved to a local directory
    ida.add_noise2wave(rand_rec_dir, prop_dir, amp_scale, rem_shadow, noisy_wave_save_dir)


    return()



