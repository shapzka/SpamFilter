# This is a program to create "bootstrap" replicate sets from a single dataset.
# This idea equates to sampling with replacement.

import numpy as np 
import random
import pandas as pd
import sys

# n_instances := number of instances to have in the replicate set.
# Returns an array holding (random  indices of data instances to put into the set.
def sampleWithReplacement(n_instances, new_instances):
    return np.random.choice(n_instances, new_instances, replace=True)
    
# Generate a single bootstrap replicate set.    
def generateReplicate(X, new_instances):
    n_instances = X.shape[0]
    
    indices = sampleWithReplacement(n_instances, new_instances)
    
    replicate = np.array([X[indices[0]]])
        
    for i in range(1, new_instances):
        sample = np.array([X[indices[i]]])
        replicate = np.concatenate((replicate, sample), axis=0)
     
    return replicate
    

# Function to generate a certain number of replicate sets.
# Currently just prints the replicates. But, will export to .csv files 
# or feed directly into bagging algorithm
def generateBootstraps(X, new_instances, n_replicates):
    for i in range(0, n_replicates):
        replicate = generateReplicate(X, new_instances)
        print replicate
        
        
# Main function to create bootstrap replicate sets.
# argv[1] := number of replicates to generate.
def main():
    if len(sys.argv) >= 2:
        n_replicates = int(sys.argv[1])
    else:
        n_replicates = 25
  
    new_instances = 5
  
    # Let's get a dataset up in this bizniz
    df_X = pd.read_csv('test.csv', header = None)
    X = np.array(df_X)
    #print X
  
    generateBootstraps(X, new_instances, n_replicates)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()