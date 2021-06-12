################################
## ---- Atmosphere Class ---- ##
################################
import matplotlib.pyplot as plt
import numpy as np
import geopandas

class atmosphere:
    def __init__(self, data, metadata):
        self.data = data
        self.metadata = metadata
    #

    def plot_effective_wind_speed(self, lat, lon, pad_lat=1, pad_lon=1, azimuths=[135, 90, 45, 180, 0, 225, 270, 315], c_pad=50):

        ##########################
        ## SOME INPUTS REQUIRED ##
        ##########################

        R = 8.314463/0.0289645 # Gas constant [J K-1 mol-1]
        gamma = 1.4 ##adiabatic index

        ## define the vertical axis
        vax = self.data[:,0]

        ## make a list of variables
        atm_var = list(self.metadata.iloc[0,:])

        ## isolate all atmospheres columns
        atm_t = self.data[:,atm_var.index(' T')]
        atm_u = self.data[:,atm_var.index(' U')]
        atm_v = self.data[:,atm_var.index(' V')]
        atm_rho = self.data[:,atm_var.index(' RHO')]
        atm_p = self.data[:,atm_var.index(' P')]

        ## calculate the static (no wind) speed of atmosphere
        c_atm =  np.sqrt(gamma * R * atm_t)

        ## place some boundaries on the sound speed (for plotting only)
        c_min = np.min(c_atm) - c_pad
        c_max = np.max(c_atm) + c_pad


        ############################
        ## GEOSPATIAL INFORMATION ##
        ############################

        ## the world dataset
        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        

        #################
        ## SET UP PLOT ##
        #################
        plt.ion()

        fig, axs = plt.subplots(3,3,figsize=(8,6))
        fig.subplots_adjust(hspace = 0.5, wspace = 0.5)

        ## set up the panel indices to plot
        t1 = [0, 1, 2]
        t2 = [0, 1 ,2]
        panel_inds = [[i, j] for i in t1 for j in t2 if not all((i == j, i==1))]

        ## loop over the propagation directions
        i=0

        while i < len(azimuths):

            ## define the current angle
            cur_angle = azimuths[i]

            ## get north and south component ratios
            n_comp = np.sin(cur_angle*np.pi/180)
            e_comp = np.cos(cur_angle*np.pi/180)

            #calculate the the effective sound speed
            cur_c = c_atm + (atm_u * e_comp) + (atm_v * n_comp)
            

            ##############
            ## PLOTTING ##
            ##############

            ## current panel
            cur_pan = panel_inds[i]

            ## plot the sound speed
            axs[cur_pan[0],cur_pan[1]].plot(cur_c, vax, c='#487998', linewidth=2.5)

            ## adjust axis
            axs[cur_pan[0],cur_pan[1]].set_xlim(c_min, c_max)

            ## add grid lines
            axs[cur_pan[0],cur_pan[1]].grid(True, 'both')

            ## add extra vertical line to note waveguides
            axs[cur_pan[0],cur_pan[1]].vlines(cur_c[0],vax[0],vax[-1],linestyles='dashed',linewidth=1.5, colors='#d8a374')

            ## add a title
            if cur_angle == 135: cur_title = 'Northwest'
            if cur_angle == 90: cur_title = 'North'
            if cur_angle == 45: cur_title = 'Northeast'
            if cur_angle == 0: cur_title = 'East'
            if cur_angle == 315: cur_title = 'Southeast'
            if cur_angle == 270: cur_title = 'South'
            if cur_angle == 225: cur_title = 'Southwest'
            if cur_angle == 180: cur_title = 'West'
            
            axs[cur_pan[0],cur_pan[1]].set_title(cur_title)

            if cur_angle in [135, 180, 225]:
                axs[cur_pan[0],cur_pan[1]].set_ylabel('Height [km]')
            #
            if cur_angle in [225, 270, 315]:
                axs[cur_pan[0],cur_pan[1]].set_xlabel('E. Sound Speed [m/s]')
            #
            
            i=i+1
        #

        ## plot the geospatial data
        world.boundary.plot(ax=axs[1,1],edgecolor='#655b59',linewidth=1.5)

        ## add the atmospheric point
        axs[1,1].scatter(lon,lat,c='black', s=50)
        axs[1,1].scatter(lon,lat,c='#f17e65', s=20)

        ## hone the map axis
        axs[1,1].set_ylim(lat - pad_lat, lat + pad_lat)
        axs[1,1].set_xlim(lon - pad_lon, lon + pad_lon)

        ## turn tha axis off
        axs[1,1].axis('off')
        
        
        
        
    #





















