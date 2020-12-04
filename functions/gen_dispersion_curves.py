#######################################
## ---- Build Dispersion Curves ---- ##
#######################################

import os
import subprocess

def gen_dispersion_curves(atm_dir, dispersion_save_dir, f_min, f_step, f_max, prop_directions, atm_order): 

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

            ## build command to create dispersion file
            dispersion_cmd = ['ModBB', '--out_disp_src2rcv_file', cur_dis_path, '--atmosfile', cur_atm_path, '--atmosfileorder', atm_order, '--azimuth', str(azimuth), '--f_min', str(f_min), '--f_step', str(f_step), '--f_max', str(f_max), '--use_modess', '--skiplines', '0']


            ## build the dispersion curve with the above command
            subprocess.run(dispersion_cmd)

            j=j+1
        #
        i=i+1
    #

    return('done generating disperion curves')














