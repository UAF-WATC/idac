####################################
## ---- Generate Atmospheres ---- ##
####################################

import os
import subprocess
import numpy as np
import idac as ida


def gen_atms(atm_build_dir, atm_save_dir, years, months, days, hours, lats, longs, zmax, dz, ap=10.0, f107=77, atm_file_name = 'default'):


    ## change to the atmosphere buidling room
    os.chdir(atm_build_dir)

    ## name all the input permutations
    all_inputs = [[i,j,k,l,m,n] for i in years for j in months for k in days for l in hours for m in lats for n in longs]

    ## loop over all the input permutations
    i=0
    while i < len(all_inputs):

        ## grab the current inputs
        cur_inputs = all_inputs[i]
        cur_year = cur_inputs[0]
        cur_month = cur_inputs[1]
        cur_day = cur_inputs[2]
        cur_hour = cur_inputs[3]
        cur_lat = cur_inputs[4]
        cur_long = cur_inputs[5]

        ## create a grid of atmospheres
        lat_longs = np.zeros((len(lats)*len(longs),2))
        lat_longs[:] = np.nan

        ## build the command
        build_atm_cmd=['probe_HWT14', str(cur_year), str(cur_month), str(cur_day), str(cur_hour), str(cur_long), str(cur_lat), str(ap), str(f107), str(zmax), str(dz)]

        ## run the command to build the atmospheres
        subprocess.run(build_atm_cmd)


        #########################################################
        ### ADD THE HEADER INFORMATION TO THE ATMOSPHERE FILE ###
        #########################################################

        ## define the header information
        ## this is formulated specifically for AVOG2S
        header = '#% 1, Z, km\n\
#% 2, T, degK\n\
#% 3, U, m/s\n\
#% 4, V, m/s\n\
#% 5, RHO, g/cm3\n\
#% 6, P, mbar\n'

        ## add the header information to the atmosphere file
        ida.add_file_header('sonde_ztuvrp.dat', header)
        



        

        ##################################################
        ## COPY THE ATMOSPHERE OUT OF THE BUILDING ROOM ##
        ##################################################

        ## prepare to save the atmosphere
        save_month = str(cur_month)
        save_day = str(cur_day)
        save_hour = str(cur_hour)

        ## check if the month, day, or hour needs a 0 in front
        if int(cur_month) < 10:
            save_month = '0' + str(cur_month)
        #
        if int(cur_day) < 10:
            save_day = '0' + str(cur_day)
        #
        if int(cur_hour) < 10:
            save_hour = '0' + str(cur_hour)
        #


        ## define what the atmospheric file name will be
        if atm_file_name == 'default':
            atm_file=str(cur_year) + save_month + save_day + save_hour + '_' + str(cur_lat) + '_' + str(cur_long) + '.dat'
        if atm_file_name != 'default':
            atm_file = atm_file_name
        #

        ## copy the data from the building room up a directory
        copy_atm_cmd = ['cp', 'sonde_ztuvrp.dat', atm_save_dir + atm_file]
        ## run the copy command
        subprocess.run(copy_atm_cmd)

        i=i+1
    #
    
    return('done generating atmospheres')

  







