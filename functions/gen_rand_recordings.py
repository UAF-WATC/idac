##########################################
## ---- Generate Random Recordings ---- ##
##########################################


import idac as ida
import numpy as np
import obspy
import matplotlib.pyplot as plt
import os
from obspy.clients.fdsn import Client
import obspy
from obspy import UTCDateTime
import random



'''
##############
### INPUTS ###
##############
 
client -- usually client = obspy.Client(base_url='IRIS')
networks -- list of strings giving the networks to sample from
stations -- list of strings giving the stations to sample from
locations -- list of strings giving the station locations to sample from (e.g. 'EP')
channels -- list of strings giving the station channels to sample from 
years -- list of strings giving the years to sample from
months -- list of strings giving the months to sample from
days -- list of strings giving the days to sample from
hours -- list of strings giving the hours to sample from
mins -- list of strings giving the minutes to sample from
secs -- list of strings giving the seconds to sample from 
n_wigs -- number of sample wiggles to generate and save 
save_dir -- directory where random wiggles will be saved 
wig_length -- time length of wiggle to generate [seconds]
n_wig_buffer -- how to scale number of n_wigs as some data will not exist [percent]


#############
### NOTES ###
#############

len(networks) == len(stations) == len(locations) == len(channels)
However len(years) doesn't have to equal len(days), len(hours), len(mins), len(secs), etc...


###############
### OUTPUTS ###
###############

obspy strems written to your local disk
'''

## create a range of times
# years = ['2012']
# months = np.arange(12)[::4] + 1  ##['1','2','3','4','5','6','7','8','9','10','11','12']
# days = [str(i) for i in (np.arange(28)+1)]
# hours = [str(i) for i in (np.arange(23)+1)]
# mins = [str(i) for i in (np.arange(59)+1)]
# secs = [str(i) for i in (np.arange(59)+1)]
# n_wigs = atm_params * src_params * dispersion_params * prop_params * 2 
# n_wig_buffer=50
# save_dir = project_dir + 'modeled_data/random_recordings/'
# wig_length=500.0

def gen_rand_recordings(client, networks, stations, locations, channels, years, months, days, hours, mins, secs, n_wigs, save_dir, wig_length, n_wig_buffer=50):

    ## keep the original number of random wiggels
    n_wigs_org = n_wigs

    ## scale the number of wiggles according to the buffer
    n_wigs = int(n_wigs * n_wig_buffer)

    ## find all permutations of the time inputs 
    all_inputs = [[i,j,k,l,m,n] for i in years for j in months for k in days for l in hours for m in mins for n in secs]

    ## randomly shuffle this list
    random.shuffle(all_inputs)

    ## define a set of UNIQUE indicies to sample all the time inputs
    ##time_inds = random.sample(range(1,len(all_inputs)-1), n_wigs)

    ## define a set of indices to sample the station inventory
    ##inventory_inds = [random.randint(0, len(networks)-1) for i in time_inds]
    inventory_inds = [random.randint(0, len(networks)-1) for i in all_inputs]
    

    ## generate n_wigs worth of random times
    j=len(os.listdir(save_dir)) ## for counting number of files generated
    i=0 ## for indexing data

    while j < n_wigs_org:

        ## define the current station inventory
        cur_network = networks[inventory_inds[i]]
        cur_station = stations[inventory_inds[i]]
        cur_location = locations[inventory_inds[i]]
        cur_channel = channels[inventory_inds[i]]
        
        ## define the current time inputs
        ##cur_time_inputs = all_inputs[time_inds[i]]
        cur_time_inputs = all_inputs[i]
        cur_time_inputs = [int(i) for i in cur_time_inputs]

        ## sample each of the time elements
        cur_year = cur_time_inputs[0]
        cur_month = cur_time_inputs[1]
        cur_day = cur_time_inputs[2]
        cur_hour = cur_time_inputs[3]
        cur_min = cur_time_inputs[4]
        cur_sec = cur_time_inputs[5]

        ## create a UTC time object
        cur_start=UTCDateTime(cur_year, cur_month, cur_day, cur_hour, cur_min, cur_sec)
        cur_stop = cur_start + wig_length

        ## try to read in the stream
        try:
            cur_stream = client.get_waveforms(cur_network, cur_station, cur_location, cur_channel, cur_start, cur_stop,attach_response=True)

            ## remove sensativity
            cur_stream.remove_sensitivity()

            ##############
            ### SAVING ###
            ##############

            ## get a good file name
            save_file=cur_network +'_'+ cur_station +'_'+ cur_location +'_'+ cur_channel +'_'+ str(cur_year) +'_'+ str(cur_month) +'_'+ str(cur_day) +'_'+ str(cur_hour) +'_'+ str(cur_min) +'_'+ str(cur_sec) + '.mseed'

            save_path = save_dir + save_file

            cur_stream.write(save_path)


        except:
            print('no data found moving on')
        #

        i=i+1
        j=len(os.listdir(save_dir))
        print(i)
    #

    return('done generating random recordings')





