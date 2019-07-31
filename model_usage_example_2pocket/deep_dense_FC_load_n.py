
import keras
import keras.backend as K

from keras.models import Model, load_model
from keras.layers import Input, merge, Activation, Dropout, Dense, concatenate, Concatenate, Flatten
from keras.layers.convolutional import Convolution1D
from keras.layers.pooling import AveragePooling1D, GlobalAveragePooling1D, MaxPool1D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2

from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

#import xgboost as xgb
from sklearn import metrics

import os
import yaml
import numpy as np
import random

import pandas as pd

from pandas import DataFrame

import pylab as pl
import matplotlib.pyplot as plt
plt.switch_backend('agg')


def randomShuffle(X, Y, seed):
    idx = [t for t in range(X.shape[0])]
    random.seed(seed)
    random.shuffle(idx)
    X = X[idx]
    Y = Y[idx]
    print()
    print('-' * 36)
    print('dimension of X after synthesis:', X.shape)
    print('dimension of Y after synthesis', Y.shape)
    print('label after shuffle:', '\n', DataFrame(Y).head())
    print('-' * 36)
    return X, Y

def randomShuffle_name(X, Y, Z, seed):
    idx = [t for t in range(X.shape[0])]
    random.seed(seed)
    random.shuffle(idx)
    X = X[idx]
    Y = Y[idx]
    Z = Z[idx]
    print()
    print('-' * 36)
    print('dimension of X after synthesis:', X.shape)
    print('dimension of Y after synthesis', Y.shape)
    print('label after shuffle:', '\n', DataFrame(Y).head())
    print('-' * 36)
    return X, Y, Z


def synData(X_0, Y_0, X_1, Y_1, time):

    X_0_syn = X_0
    Y_0_syn = Y_0
    for i in range(time - 1):
        X_0_syn = np.vstack( (X_0_syn, X_0) )
        Y_0_syn = np.hstack( (Y_0_syn, Y_0) )

    print('dimension of generation data of X', X_0_syn.shape)
    print('dimension of generation data of Y', Y_0_syn.shape)
    print('dimension of generation data of X with label of 1', X_1.shape)
    print('dimension of generation data of Y with label of 1', Y_1.shape)

    #synthesis dataset
    X_syn = np.vstack( (X_0_syn, X_1) )
    Y_syn = np.hstack( (Y_0_syn, Y_1) )

    print()
    print('dimension of X after combination', X_syn.shape)
    print('dimension of Y after combination', Y_syn.shape)
    print(DataFrame(Y_syn).head())

    #shuffle data
    X_syn, Y_syn = randomShuffle(X_syn, Y_syn, 1)

    return X_syn, Y_syn


def synData_n(X_0, Y_0, Z_0, X_1, Y_1, Z_1, time):

    X_0_syn = X_0
    Y_0_syn = Y_0
    Z_0_syn = Z_0
    for i in range(time - 1):
        X_0_syn = np.vstack( (X_0_syn, X_0) )
        Y_0_syn = np.hstack( (Y_0_syn, Y_0) )
        Z_0_syn = np.hstack( (Z_0_syn, Z_0) )

    print('dimension of generation data of X', X_0_syn.shape)
    print('dimension of generation data of Y', Y_0_syn.shape)
    print('dimension of generation data of X with label of 1', X_1.shape)
    print('dimension of generation data of Y with label of 1', Y_1.shape)
    print('dimension of generation data of Z',Z_0_syn.shape)
    print('dimension of generation data of Z with label 1',Z_1.shape)
    #synthesis dataset
    X_syn = np.vstack( (X_0_syn, X_1) )
    Y_syn = np.hstack( (Y_0_syn, Y_1) )
    Z_syn = np.hstack( (Z_0_syn, Z_1) )
    print()
    print('dimension of X after combination', X_syn.shape)
    print('dimension of Y after combination', Y_syn.shape)
    print(DataFrame(Y_syn).head())

    #shuffle data
    X_syn, Y_syn, Z_syn = randomShuffle_name(X_syn, Y_syn, Z_syn, 1)

    return X_syn, Y_syn, Z_syn



mp_data='mp_data'

pos_samples = np.array(pd.read_hdf(mp_data+'/pos.h5', 'df'), dtype=float)
pos_labels = np.ones(pos_samples.shape[0])

pos_list_used=pd.read_csv(mp_data+'/pos_list.csv', header = 0)




seed=1

pos_names=pos_list_used.values.reshape(-1)

print  pos_names.shape, pos_labels.shape

test_pos_samples = pos_samples[:,  :]
test_pos_names = pos_names[:]





test_X = test_pos_samples.astype(np.float64)



def preprocess_data_train(data_set):
    mean = -0.5696
    std = 30.8744
    t = data_set
    t -= mean
    t /= std
    return t


def preprocess_data(data_set):
    mean = np.mean(data_set)
    std = np.std(data_set)
    
    t = data_set

    t -= mean
    t /= std
    return t

def aucJ(true_labels, predictions):
    
    fpr, tpr, thresholds = metrics.roc_curve(true_labels, predictions, pos_label=1)
    auc = metrics.auc(fpr,tpr)

    return auc

def acc(true, pred):
    
    return np.sum(true == pred) * 1.0 / len(true)

def assess(model, X, label, thre = 0.5):
    
    threshold = thre
    
    pred = model.predict(X)
    pred = pred.flatten()
    
    pred[pred > threshold] = 1
    pred[pred <= threshold] = 0
    
    auc = aucJ(label, pred)
    accuracy = acc(label, pred)
    
    print('auc: ', auc)
    print('accuracy: ', accuracy)




test_X = preprocess_data_train(test_X)





#assess(model, test_X, test_Y)

model=load_model('FCdenset_near.h5')

#model = load_model('FCdenset.h5')



def aucFigureS(label, pred, name):

    fpr, tpr, thresholds = metrics.roc_curve(label, pred, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    model_name="DeepBindRG"
    plt.plot(fpr, tpr, lw = 1, label = 'auc(%.4f)' % auc)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.legend(loc = 'best')
    pl.title("ROC curve of %s" % model_name)
    pl.xlabel("False Positive Rate")
    pl.ylabel("True Positive Rate")
    #plt.show()
    plt.plot([0,1],[0,1],'--', color=(0.6,0.6,0.6), label='luck')
    plt.savefig(name)



##########################################################
##########################################################

#########################################################
#########################################################

pred = model.predict(test_X)
pred = pred.flatten()

outcontent=[]
for i in  range(len(test_pos_names)):
        outcontent.append(test_pos_names[i]+'  '+str(pred[i]))

outcontent=DataFrame(outcontent, columns=['all'])
new = outcontent['all'].str.split(" ", n = 1, expand = True)

outcontent2=DataFrame()
outcontent2["name"]= new[0]
outcontent2["prediction"]= new[1].astype('float')
result=outcontent2.sort_values(by=["prediction"],ascending=False)

result.to_csv('out_list.csv', index = False)

#########################################################
#########################################################



