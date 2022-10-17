#!/usr/bin/env python3
import pandas as pd
import os
import itertools 
import numpy as np
import csv
#Created By Adithya Shastry
#Email: ams2590@cumc.columbia.edu
DEBUG = True



class EEGProcessing:
    '''
    This class will have various functions requried to process the
    EEG data given in the tfc file format
    '''
    def __init__(self):
        pass

    def loadtfc(self,file,sources=["e0","e1","e2"]):
        '''
        Will load the tfc file and return it as a dictionary of 2d arrays
        where each 2d array is different source.
        Inputs:
            - file: The file to be loaded in (should be a full file path)
            - sources: What you want to name the sources in the dictionary
        '''
        sourceCount = 0
        outputDict = {}
        for source in sources:
            outputDict[source] = []#Initialize the 

        #First we want to read the file in and store the data for processing
        with open(file,'r') as f:
            reader = csv.reader(f,delimiter='\t')
            next(reader)#we want to skip the header
            next(reader)
            for line in reader:
                if len(line) <= 1:
                    #We have a empty space denoting the start of a new source
                    sourceCount += 1
                    continue

                #We want to read in each line and store to a list
                outputDict[list(outputDict.keys())[sourceCount]].append(line[:-1])
        for key,value in outputDict.items():
            #print(len(value),len(value[0]))
            outputDict[key] = np.array(value)
            print(key,outputDict[key].shape)


            
        

                
         
                
        return outputDict

if __name__ == '__main__':

    eeg = EEGProcessing()
    
    ###WRITE COMMANDS TO CHECK loadtfc
    #Cd into a directory to check the function
    directory = "/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/EEG Data/TSE paper2/Controls Source TSE/Anode1 and2" 
    for f in os.listdir(directory):
        if not f.endswith('.tfc'):
            #we dont care about this file so continue
            continue
        #call the function
        print(f)
        eeg.loadtfc(os.path.join(directory,f))

