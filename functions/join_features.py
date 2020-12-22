#############################
## ---- Join Features ---- ##
#############################

import idac as ida
import numpy as np
import pandas as pd
import pickle


def join_features(features):

    ## loop over the length of features
    i=0
    while i < len(features):

        ## pull out the current features
        cur_features = features[i]

        ## creat an array of labels
        cur_labs = np.zeros([cur_features.shape[0],1]) + i

        ## add labels to featuers
        cur_feature_labels=np.concatenate([cur_features,cur_labs],axis=1)

        ## initilize a labeled features if this is first iteration
        if i == 0:
            labeled_features = cur_feature_labels
        #
        if i > 0:
            labeled_features = np.concatenate([labeled_features, cur_feature_labels], axis=0)
        #

        i=i+1
    #
    
    ## convert to a pandas dataframe
    labeled_features_df = pd.DataFrame(labeled_features)


    ## define some column names
    col_names = ['feature_' + str(i) for i in np.arange(labeled_features.shape[1])]

    ## change the last column name to category_id
    col_names[-1] = 'category_id'

    ## add the column names to the pandas dataframe
    labeled_features_df.columns = col_names

    return(labeled_features_df)



# ## create an array of labels
# rand_labels = np.zeros((synth_features.shape[0],1))
# synth_labels = np.zeros((synth_features.shape[0],1)) + 1 

# ## add labels to the features
# synth_features_labels = np.concatenate([synth_features, synth_labels],axis=1)
# rand_features_labels = np.concatenate([rand_features, rand_labels],axis=1)

# ## join all features
# labeled_features = np.concatenate([synth_features_labels, rand_features_labels], axis=0)

# ## convert to a pandas dataframe
# labeled_features_df = pd.DataFrame(labeled_features)

# ## define some column names
# col_names = ['feature_' + str(i) for i in np.arange(labeled_features.shape[1])]

# ## change the last column name to category_id
# col_names[-1] = 'category_id'

# ## add the column names to the pandas dataframe
# labeled_features_df.columns = col_names

