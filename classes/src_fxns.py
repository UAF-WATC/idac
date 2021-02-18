##########################################
## ---- Source Time Function Class ---- ##
##########################################


from scipy import fft
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

class src_fxns:
    def __init__(self, data):
        self.data = data
    #

    def plot(self, t_xlims=[0,5], f_xlims=[0,5]):

        ## make sure the data are in both an np array and pd dataframe
        data_arr = np.array(self.data)
        data_df = pd.DataFrame(self.data)

        
        ## extract the time axis
        tax = data_arr[:,0]
        
        ######################
        ## FREQUENCY DOMAIN ## 
        ######################

        time = np.max(tax) - np.min(tax)
        df = 1/time
        fax = np.arange(len(tax))*df + df

        ## define a quick function to take to the frequency domain
        fd = lambda a : np.abs(fft.fft(a))

        ## make a copy of data for the frequency domain components
        DATA = data_arr[:]

        ## apply the frequency domain lampda function to each column
        DATA = np.apply_along_axis(fd, 0, DATA)

        ## replace the first column with the frequency axis
        DATA[:,0] = fax
        

        #####################
        ## SET UP THE PLOT ## 
        #####################
        plt.ion()


        ## copy the pandas dataframe
        DATA_df = pd.DataFrame(DATA)
        DATA_df.columns = ['frequency [Hz]'] + list(data_df.columns[1:])

        ## melt... the dataframe from long form to short form
        time_id_col = data_df.columns[0]
        freq_id_col = DATA_df.columns[0]
        
        data_melt = data_df.melt(time_id_col, var_name='weights [Kg]', value_name='pressure [Pa]')
        DATA_melt = DATA_df.melt(freq_id_col, var_name='weights [Kg]', value_name='amplitude')
        
        
        fig, axs = plt.subplots(1,2)

        sns.lineplot(ax=axs[0], x=time_id_col, y='pressure [Pa]', hue='weights [Kg]', data=data_melt, ci=None, legend=False, linewidth=2, palette='crest')
        axs[0].set_xlim(t_xlims)

        sns.lineplot(ax=axs[1], x=freq_id_col, y='amplitude', hue='weights [Kg]', data=DATA_melt, ci=None, legend='full', linewidth=2, palette='crest')
        axs[1].set_xlim(f_xlims)
    #
    

