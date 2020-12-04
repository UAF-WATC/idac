######################################################
## ---- Propagate Waveform through Atmospheres ---- ##
######################################################


import numpy as np
import subprocess
import os

def prop_waveforms(dispersion_dir, source_time_fxn_dir, atm_dir, prop_dists, max_celerity, prop_wave_dir):

    ## list all the files
    dispersion_files_all = os.listdir(dispersion_dir)
    source_time_fxn_files_all = os.listdir(source_time_fxn_dir)
    atm_files_all = os.listdir(atm_dir)

    ## remove anything that isn't data
    dispersion_files = [i for i in dispersion_files_all if '.dat' in i]
    source_time_fxn_files = [i for i in source_time_fxn_files_all if '.dat' in i]
    atm_files = [i for i in atm_files_all if '.dat' in i]

    ## loop over the dispersion files
    i=0
    while i < len(dispersion_files):

        ## loop over ther source time functions
        j=0
        while j < len(source_time_fxn_files):

            ## loop over the propagation distances
            k=0
            while k < len(prop_dists):

                ## grab the current propagation (range distance)
                range_dist = prop_dists[k]

                ## grab the current file
                cur_dispersion_file = dispersion_files[i]
                cur_source_time_fxn_file = source_time_fxn_files[j]
                #cur_atm_file = atm_files[0]

                ## grab the files/paths
                cur_dispersion_path = dispersion_dir + cur_dispersion_file
                cur_source_time_fxn_path = source_time_fxn_dir + cur_source_time_fxn_file
                ##cur_atm_path = atm_dir + cur_atm_file

                ## make a file with SourceTimeFxn_YearMonthDayHour_Lat_Long format
                prop_wave_file = cur_source_time_fxn_file[:-4] + '_' +  cur_dispersion_file[:-4] + '_' + str(range_dist) + '.dat'

                ## define propagated wave path
                prop_wave_path = prop_wave_dir + prop_wave_file


                ## write the command to do the propagation
                prop_cmd = ['ModBB', '--pulse_prop_src2rcv', cur_dispersion_path, '--range_R_km', str(range_dist), '--waveform_out_file', prop_wave_path, '--src_waveform_file', cur_source_time_fxn_path, '--max_celerity', str(max_celerity)]


                ## run the wave prop command
                subprocess.run(prop_cmd)

                k=k+1
            #
            j=j+1
        #
        i=i+1
    #

    return('done propagating waveforms')









