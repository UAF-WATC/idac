################################
## ---- Run Vanilla ANNN ---- ##
################################


#Dependencies
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

#from keras.models import load_model
#from sklearn.metrics import accuracy_score


def train_vanilla_ann(labeled_features, num_epochs=5, norm_features=True):

    
    ###############################
    ## PREPROCESSING AND SCALING ##
    ###############################

    ## remove any nan values
    ##labeled_features = labeled_features[~np.isnan(labeled_features).any(axis=1)]
    labeled_features = labeled_features[~pd.isnull(labeled_features).any(axis=1)]

    # isolate the features and the labels from the dataframe
    features = labeled_features.drop(labels='category_id',axis=1)
    labels_raw = labeled_features['category_id']

    ## reshape labels from a column 'vector' to row 'vector'
    labels_raw = np.array(labels_raw).reshape(len(labels_raw),1)

    if norm_features == True:
        ## Normalize the data (mean=0 and std=1)
        sc = StandardScaler()
        features = sc.fit_transform(features)
    #    

    # one hot encode the raw labels
    ohe = OneHotEncoder()
    labels = ohe.fit_transform(labels_raw).toarray()

    ## split the data into a training and test set
    features_train, features_test,labels_train,labels_test = train_test_split(features,labels,test_size = 0.2,shuffle=True)

    ##################
    ## BUILD THE NN ##
    ##################
    ## Neural network architecture

    ## tells keras to create a model sequentially
    model = Sequential()

    ## add each layer to the ANN (Dense = fully connected)
    model.add(Dense(features.shape[1], input_dim=features.shape[1], activation="relu"))
    


    ##model.add(Dense(features.shape[1], activation="relu"))
    ##model.add(Dense(features.shape[1], activation="relu"))



    
    model.add(Dense(labels.shape[1], activation="softmax"))
    ##model.add(Dense(labels.shape[1], activation="sigmoid"))

    ## specify the loss function and optimizer using compile functions
    ##model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])


    #####################
    ### TRAIN THE ANN ###
    #####################

    history = model.fit(features_train, labels_train, validation_data = (features_test,labels_test), epochs=num_epochs, batch_size=64)

    ## return the model, scaling factors, and training history.
    if norm_features == True:
        return([model, sc, history, (features_test,labels_test)])
    #
    if norm_features == False:
        return([model, history,(features_test,labels_test)])
    #
#




