##########################################################################
## ---- Infrasound Data Augmentation and Classification Parameters ---- ##
##########################################################################

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

atm_years = [2012]
atm_months = [8]
atm_days = [1]
atm_hours = [17]
atm_lats = np.linspace(30, 50, 4)
atm_longs = np.linspace(70, 120, 4)

ap = 10.0 ## geomagnetic planetary index (best to leave alone) 
f107 = 77 ## solar radio flux (best to leave alone)
zmax = 200 ## max altitude [km] 
dz = 0.1 ## vertical resolution [km]


#######################################
## FRIEDLANDER SOURCE TIME FUNCTIONS ##
#######################################

amps = [4000, 8000, 12000, 16000] ## amplitudes 
tss = [0.1, 0.5, 1., 1.5, 2., 2.5] # first zero crossing 
time = 500 # time length of waveform [secs] 
dt = 1 ## sampling frequency [secs]


#######################
## Dispersion Curves ##
#######################

f_min = 0.002 ## frequency min
f_step = 0.002 ## frequency step
f_max = 0.5 ## frequency max

## array of propagation directions
prop_directions = [0, 90, 180, 270]


##########################
### PROPAGATE WAVEFORM ###
##########################

prop_dists = [100, 150, 200, 250, 300, 350, 400] ## [km]
max_celerity = 340 # [m/s]


##################################
### GENERATE RANDOM RECORDINGS ###
##################################

client = Client(base_url='IRIS')

## station information
network = 'TA'
station = 'W18A'
location = 'EP'
channel = 'BDF'

## create a range of times
rand_years = ['2012']
rand_months = ['08']
rand_days = [str(i) for i in (np.arange(30)+1)]
rand_hours = [str(i) for i in (np.arange(23)+1)]
rand_mins = [str(i) for i in (np.arange(59)+1)]
rand_secs = [str(i) for i in (np.arange(59)+1)]

## propagated waveform files
prop_files = os.listdir(prop_wave_dir)

## how many random wiggles do you need?
## generate twice as many for both events and non events
n_rand_wigs = len(prop_files) * 2 


##################################
## ADD NOISE TO PROPAGATED WAVE ##
##################################

## how to scale the amplitudes
## this is bad and should be addressed soon
amp_scale = 1000

## do you want to remove propagated waves within a "shadow zone"
## this is bad and should be addressed soon
rem_shadow = True









