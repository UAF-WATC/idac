###############################################
## ---- Fit Roger Wave to Recorded Data ---- ##
###############################################

import numpy as np
import scipy
import obspy 

from scipy.optimize import curve_fit

def fit_roger2data(data, sps, init_guess=[]):

    ## create a time axis
    tax = np.arange(len(data)) / sps + 1/sps

    if len(init_guess) == 0:
        init_guess = np.array([100, 1, 1/(6*np.pi), 8])
    #

    
    ## define function according to equations (15.38) and (15.39)
    def source_time_fxn(t, a, fc, w0, beta):

        ## define expression given by equation (15.38)
        def f(x, beta):
            wig = x**beta * (1-x/(1+beta))*np.exp(-x)
            return(wig)

        ## define the max of f
        x0 = (1+beta) * (1-(1/(1+beta)**(1/2))) # max amplitude of f

        ## calculate the source time function according to (15.39)
        stf = a * f(fc/w0*t, beta) / f(x0, beta)

        return(stf)


    ## define function according to equations (15.38) and (15.39)
    def SOURCE_TIME_FXN(t, a, fc, w0, beta):

        ## define expression given by equation (15.38)
        def f(x, beta):
            wig = x**beta * (1-x/(1+beta))*np.exp(-x)
            return(wig)

        ## define the max of f
        x0 = (1+beta) * (1-(1/(1+beta)**(1/2))) # max amplitude of f

        ## calculate the source time function according to (15.39)
        stf = a * f(fc/w0*t, beta) / f(x0, beta)

        ## frequency domain
        STF = np.abs(np.fft.fft(stf))

        return(STF)


    ## Bring the data into the frequency domain
    DATA = np.abs(np.fft.fft(data))

    ## fit the parameters to the data
    popt, pcov = curve_fit(SOURCE_TIME_FXN, tax, DATA, p0=init_guess)

    ## extract the Fitted parameters
    amp = popt[0] ## amplitude 
    fc = popt[1] #8 # controls rise time and zero crossing of impulse
    w0 = popt[2] #1/(np.pi*6)#0.4776 # max angular frequency of f
    beta = popt[3] #1  # [Hz]

    roger_wave = source_time_fxn(tax, amp, fc, w0, beta)

    return(roger_wave)












