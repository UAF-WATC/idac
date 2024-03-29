#######################################
## ---- Build Dispersion Curves ---- ##
#######################################

import os
import subprocess

def gen_dispersion_curves(atm_dir, dispersion_save_dir, f_min, f_step, f_max, prop_directions, disp_method='modess', which_cores = False, wvnum_filter=False, c_min='', c_max=''): 

    ## list only the atmospheric files 
    all_atm_files = os.listdir(atm_dir)
    atm_files = [i for i in all_atm_files if '.dat' in i]

    ## loop over the atmospheric files and propagation directions
    i=0
    while i < len(atm_files):

        ## loop over the propagation directions
        j=0
        while j < len(prop_directions):

            ## grab all the inputs

            ## what is the current atmsophere path
            cur_atm_path = atm_dir + atm_files[i]

            ## azimuth
            azimuth = prop_directions[j]

            ## filename of dispersion curve
            dispersion_file = atm_files[i][:-4] + '_' + str(prop_directions[j]) + '.dat'

            ## what is the current dispersion save path
            cur_dis_path = dispersion_save_dir + dispersion_file

            ## build base command
            dispersion_cmd = ['ModBB', '--dispersion', '--dispersion_file', cur_dis_path, '--atmosfile', cur_atm_path, '--azimuth', str(azimuth), '--method', disp_method, '--f_min', str(f_min), '--f_step', str(f_step), '--f_max', str(f_max)]
            # ## check if you want to run ModBB on particular cores
            # if which_cores == False:
            #     ## build command to create dispersion file
            #     ##dispersion_cmd = ['ModBB', '--dispersion', '--dispersion_file', cur_dis_path, '--atmosfile', cur_atm_path, '--azimuth', str(azimuth), '--method', disp_method, '--f_min', str(f_min), '--f_step', str(f_step), '--f_max', str(f_max)]
            #     dispersion_cmd = dispersion_cmd
            # #

            ## check if you want to run ModBB on particular cores
            if which_cores != False:
                ## build the command specify which cores to run on 
                ##dispersion_cmd = ['taskset', '-c', which_cores, 'ModBB', '--dispersion', '--dispersion_file', cur_dis_path, '--atmosfile', cur_atm_path, '--azimuth', str(azimuth), '--method', disp_method, '--f_min', str(f_min), '--f_step', str(f_step), '--f_max', str(f_max)]
                dispersion_cmd = ['taskset', '-c', which_cores] + dispersion_cmd
            #

            ## check if you want to perform wavenumber filtering
            if wvnum_filter == True:
                dispersion_cmd = dispersion_cmd + ['--wvnum_filter', '--c_min', str(c_min), '--c_max', str(c_max)]
            #
            
            ## build the dispersion curve with the above command
            subprocess.run(dispersion_cmd)

            j=j+1
        #
        i=i+1
    #

    return('done generating disperion curves')














