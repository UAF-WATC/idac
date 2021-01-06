##########################################################################
## ---- Infrasound Data Augmentation and Classification Parameters ---- ##
##########################################################################

import numpy as np
import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime



## Inputs in this file will reproduce the data used in Witsil et al. (2021).

'''
File containing all needed input parameters to run infrasound data augmentation.
This file is meant to be an input into idac.run_ida. 
Note the function idac.run_ida runs a series of functions.
Each step in the workflow writes (potentially voluminous amounts of) data to your disk.
Please take care there is enough disk space prior to running.

The workflow is as follows: 

generate atmospheres (via idac.gen_atms)

|
v

generate source time functions (via idac.gen_friedlander)

|
v 

generate_dispersion_curves (via idac.gen_dispersion_curves)

|
v

propagate_waveforms (via idac.prop_waveforms)

|
v

generate_random_recordings (via idac.gen_rand_recordings)

|
v

add_noise_to_propagated_wave (via idac.add_noise)

'''


#################################
### WRITING and READING PATHS ###
#################################

## base directory for the current project
project_dir = '/home/alex/projects/idac_projects/test/'

## where to build and save the atmospheres
atm_save_dir = project_dir + 'modeled_data/atmospheres/'
atm_build_dir = atm_save_dir + 'building_room'

## where to save source time functions
source_time_fun_save_dir = project_dir + 'modeled_data/source_time_fxns/'

## where to save the dispersion curves
dispersion_save_dir = project_dir + 'modeled_data/dispersion_curves/'

## where to save the propagated waveform_out_file
prop_wave_dir = project_dir + 'modeled_data/propagated_waves/'

## where to save the random recordings 
rand_save_dir = project_dir + 'modeled_data/random_recordings/'

## where to save the noise_added waveforms
noisy_wave_save_dir = project_dir + 'modeled_data/synthetic_events/'


############################
## Atmosphere Parameteers ##
############################

atm_years = [2012] ## {Blom et al. (2018)}
atm_months = [3, 6, 9, 12] ## {Blom et al. (2015)}
atm_days = [20]
atm_hours = [12]
atm_lats = list(range(25, 55, 5))
atm_longs = list(range(-120, -60, 10))


##DME##
# lat_long_grid = [[i,j] for i in atm_lats for j in atm_longs]
# lat_long_array = np.zeros((len(lat_long_grid),2))

# i=0
# while i < len(lat_long_grid):
#     lat_long_array[i,0] = lat_long_grid[i][0]
#     lat_long_array[i,1] = lat_long_grid[i][1]

#     i=i+1
# #

# np.savetxt('/home/alex/Desktop/lat_longs.txt', lat_long_array)




ap = 10.0 ## geomagnetic planetary index (best to leave alone) 
f107 = 77 ## solar radio flux (best to leave alone)
zmax = 90 ## max altitude [km] ## {Blom et al. (2018)}
dz = 0.1 ## vertical resolution [km]


#######################################
## FRIEDLANDER SOURCE TIME FUNCTIONS ##
#######################################

weights = list(range(0, 550, 50)) ## weights of charge [kg] {Blom et al. (2018)}
time = 500 # time length of waveform [secs] 
dt = 1 ## sampling frequency [secs]


#######################
## Dispersion Curves ##
#######################

f_min = 0.002 ## frequency min [Hz] {Blom et al. (2018)}
f_step = 0.002 ## frequency step. Also note total length = 1/f_step [Hz]
f_max = 2.5 ## frequency max [Hz] {Blom et al. (2018)}

## array of propagation directions
prop_directions = [45, 90, 135, 180, 225, 270, 315, 360] ## [degrees] {Blom et al. (2018)}


##########################
### PROPAGATE WAVEFORM ###
##########################

##prop_dists = [100, 150, 200, 250, 300, 350, 400] ## [km]
prop_dists = list(range(50,1050,50)) ## [km] {Blob et al. (2018)}
max_celerity = 340 # [m/s]


##################################
### GENERATE RANDOM RECORDINGS ###
##################################

client = Client(base_url='IRIS')

## create a range of times
rand_years = ['2012']
rand_months = ['1','2','3','4','5','6','7','8','9','10','11','12']
rand_days = [str(i) for i in (np.arange(30)+1)]
rand_hours = [str(i) for i in (np.arange(23)+1)]
rand_mins = [str(i) for i in (np.arange(59)+1)]
rand_secs = [str(i) for i in (np.arange(59)+1)]

## find the start time and end time over the time range
start_time = UTCDateTime(int(rand_years[0]), int(rand_months[0]), int(rand_days[0]), int(rand_hours[0]), int(rand_mins[0]), int(rand_secs[0]))
end_time = UTCDateTime(int(rand_years[-1]), int(rand_months[-1]), int(rand_days[-1]), int(rand_hours[-1]), int(rand_mins[-1]), int(rand_secs[-1]))

## find the min and max lat and longs
min_lat = np.min(atm_lats)
max_lat = np.max(atm_lats)
min_long = np.min(atm_longs)
max_long = np.max(atm_longs)

## find the station inventory
station_inventory = client.get_stations(network="*", station="*", channel="BDF", starttime=start_time, endtime=end_time, minlatitude=min_lat, maxlatitude=max_lat, minlongitude=min_long, maxlongitude=max_long, level='channel')
all_contents = station_inventory.get_contents()['channels']

## split the inventory contents up
all_contents_split = [i.split('.') for i in all_contents]

## grab the networks, stations, locations and channels
networks = [i[0] for i in all_contents_split]
stations = [i[1] for i in all_contents_split]
channels = [i[3] for i in all_contents_split]

## locations are bit harder to get because they might not exist
raw_locations = [i[2] for i in all_contents_split]
locations = ['--' if len(i) == 0 else i for i in raw_locations]

## determine the number of required random recordings by...
## the number of parameters used in the entire workflow

atm_params = len(atm_years) * len(atm_months) * len(atm_days) * len(atm_hours) * len(atm_lats) * len(atm_longs)
src_params = len(weights)
dispersion_params = len(prop_directions)
prop_params = len(prop_dists)


## generate twice as many for both events and non events
n_rand_wigs = atm_params * src_params * dispersion_params * prop_params * 2 


##################################
## ADD NOISE TO PROPAGATED WAVE ##
##################################

## how to scale the amplitudes
## this is bad and should be addressed soon
amp_scale = 1000

## do you want to remove propagated waves within a "shadow zone"
## this is bad and should be addressed soon
rem_shadow = True









