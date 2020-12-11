####################################
## ---- Example 1 Input File ---- ##
####################################


#######################
## Atmosphere Inputs ##
#######################

## time and location of atmospheres
atm_years = [2012]
atm_months=[8]
atm_days = [1]
atm_hours = [17]
atm_lats = 37.2431
atm_longs = 115.7930

zmax = 200 # max heigh of atmosphere and 
dz = 0.1 # vertical sampling resolution of atmosphere

## solar activity -- best to keep these as they are 
ap = 10.0
f107 = 77

## where to build and save the atmospheres
atm_save_dir = project_dir + 'modeled_data/atmospheres/'
atm_build_dir = atm_save_dir + 'building_room'


##############################
### DISPERSION CURVE INPUTS ##
##############################

f_min = 0.002 ## frequency min
f_step = 0.002 ## frequency step
f_max = 0.25 ## frequency max

## order of atmospheric data
atm_order = 'ztuvdp'

## array of propagation directions
prop_directions = [0]

## where are the atmospheric data to use 
atm_dir = project_dir + 'modeled_data/atmospheres/'

## where to save the dispersion curves
dispersion_save_dir = project_dir + 'modeled_data/dispersion_curves/'


###################################
### SOURCE TIME FUNCTION INPUTS ###
###################################

## where to save source time functions
save_dir = project_dir + 'modeled_data/source_time_fxns/'

## friedlander inputs 
amps = [12000]
tss = [0.5]
time = 500 # [secs]
dt = 1


###################################
### WAVEFORM PROPAGATION INPUTS ###
###################################

prop_dists = [200, 400]
max_celerity = 340 #m/s

## find the dispersion file, source time functions and atmospheres
dispersion_dir = project_dir + 'modeled_data/dispersion_curves/'
source_time_fxn_dir = project_dir + 'modeled_data/source_time_fxns/'
atm_dir = project_dir + 'modeled_data/atmospheres/'

## where to save the propagated waveform_out_file
prop_wave_dir = project_dir + 'modeled_data/propagated_waves/'


###############################
### RANDOM RECORDING INPUTS ###
###############################

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
prop_dir = project_dir + 'modeled_data/propagated_waves/'
prop_files = os.listdir(prop_dir)

## how many random wiggles do you need?
n_wigs = len(prop_files)

## generate twice as many for both events and non events
n_wigs = n_wigs*2 

## where to save the random recordings 
rand_save_dir = project_dir + 'modeled_data/random_recordings/'


##########################################
## ADD NOISE TO PROPAGATED WAVE INPUTS ###
##########################################

## how to scale the amplitudes
## this is bad and should be addressed soon
amp_scale = 1000

## do you want to remove propagated waves within a "shadow zone"
## this is bad and should be addressed soon
rem_shadow = True

## where are the random recordings and propagated waveform files
rand_rec_dir = project_dir + 'modeled_data/random_recordings/'
prop_dir = project_dir + 'modeled_data/propagated_waves/'

noisy_wave_save_dir = project_dir + 'modeled_data/synthetic_events/'





