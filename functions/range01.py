import numpy as np

def range01(data):

    scaled_data =(data - np.min(data)) / (np.max(data) - np.min(data))

    return(scaled_data)


