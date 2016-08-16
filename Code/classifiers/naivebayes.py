# coding: utf-8

'''
Adapted from: https://github.com/galvanic/adversarialML/blob/master/classifiers/naivebayes.py

Inspired by Luis Munoz's MATLAB code for the Naive Bayes classifier model.
/!\ run with python3
'''
import numpy as np
import pandas as pd
from metrics import computeError
from metrics import computeMetrics
from sklearn.naive_bayes import BernoulliNB

def process_parameters(p, tolerance=1e-10):
    '''
    Helper function for training naivebayes.
    Returns parameters where NaNs, zeros and ones have been modified to avoid
    under/overflows (??)
    Helper function for the training function.
    TODO write better docstring and explanation
    '''
    p[np.isnan(p)] = tolerance
    p[p == 0]      = tolerance
    p[p == 1]      = 1 - tolerance
    return p


def fit(features, labels,
        ## params
        ham_label=0,
        spam_label=1,
        ):
    '''
    Returns the parameters for a Naive Bayes model
    Logs are used because otherwise multiplications of very small numbers,
    which leads to problems of over/underflows
    TRAINING PHASE
    Inputs:
    - features: N * D Numpy matrix of binary values (0 and 1)
        with N: the number of training examples
        and  D: the number of features for each example
    - labels:   N * 1 Numpy vector of binary values (0 and 1)
    Outputs:
    - parameters
    '''
    ## setup
    X, Y = features, labels
    N, D = X.shape    ## number of N: training samples, D: features
    tolerance = 1e-30 ## tolerance factor (to avoid under/overflows)

    ## estimate prior probability of spam class
    prior_spam = np.sum(Y == spam_label) / np.float(N)
    prior_ham  = 1 - prior_spam

    indices_ham  = np.nonzero(Y ==  ham_label)[0]
    indices_spam = np.nonzero(Y == spam_label)[0]
    N_ham  = len(indices_ham)
    N_spam = len(indices_spam)

    ## estimate likelihood parameters for each class
    ## looks at presence of features in each class
    likeli_ham  = np.sum(X[indices_ham],  axis=0) / np.float(N_ham)
    likeli_spam = np.sum(X[indices_spam], axis=0) / np.float(N_spam)

    likeli_ham, likeli_spam = map(lambda p: p.reshape((D, 1)), [likeli_ham, likeli_spam])
    likeli_ham, likeli_spam = map(process_parameters, [likeli_ham, likeli_spam])

    return prior_ham, prior_spam, likeli_ham, likeli_spam


def predict(features, parameters,
        ## params
        ham_label=0,
        spam_label=1,
        ):
    '''
    TEST PHASE
    Inputs:
    - parameters: model parameters
    - features
    Outputs:
    - predicted: labels
    '''
    ## notation
    prior_ham, prior_spam, likeli_ham, likeli_spam = parameters
    X = features
    N, D = X.shape

    ## apply model
    ## Bernouilli Naive Bayes, takes into account absence of a feature
    log_posterior_ham  = np.log(prior_ham) +                    \
                         np.dot(   X,  np.log(  likeli_ham)) +  \
                         np.dot((1-X), np.log(1-likeli_ham))
    log_posterior_spam = np.log(prior_spam)   +                 \
                         np.dot(   X,  np.log(  likeli_spam)) + \
                         np.dot((1-X), np.log(1-likeli_spam))

    ## no need to normalise since we are just interested in which
    ## posterior is higher (ie. which label is most likely given the data)

    log_posterior_ham, log_posterior_spam = map(np.ravel, [log_posterior_ham, log_posterior_spam])
    ## calculate output
    ## assign class which is most likely over the other
    ## this works because labels are 0 and 1 for ham and spam respectively
    predicted = (log_posterior_spam > log_posterior_ham)

    if ham_label == -1:
        predicted = predicted * 2 - 1

    return np.array(predicted).astype(int) #To match the format of my other classifiers and for bagging

def main():
    '''Test NaiveBayes training'''

    df_x = pd.read_csv('../Datasets/TrainData/lingspam/X_train_1.csv', header = None)
    x = np.array(df_x)
    
    df_y = pd.read_csv('../Datasets/TrainData/lingspam/y_train_1.csv', header = None)
    y = np.array(df_y)
   
    df_x_test = pd.read_csv('../Datasets/TestData/lingspam/X_test_1.csv', header = None)
    x_test = np.array(df_x_test)
    
    df_y_test = pd.read_csv('../Datasets/TestData/lingspam/y_test_1.csv', header = None)
    y_test = np.array(df_y_test)
   
    ## train model
    weights = fit(x, np.ravel(y))        

    predictions = predict(x_test, weights)
    
    print computeError(y_test, predictions)
    print 'MY METRICS:', computeMetrics(y_test, predictions)
    
    classifier = BernoulliNB()
    classifier.fit(x, np.ravel(y))
    pred = classifier.predict(x_test)
    
    print computeError(y_test, pred)
    print computeMetrics(y_test, pred)
    return

if __name__ == '__main__':
    main()