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
            if DEBUG:
                print(key,outputDict[key].shape)
        return outputDict
    def findWindowAvg(self,outputDir,directories=None,window=(18,12,-100,0),dim1Values=(50,4,-2),dim2Values=(-400,200,25)):
        '''
        This method will find the wondow averages for directories of tfc files
        Inputs:
            - directories: the directories of tfc files to consider
            - outputDir: where to store the final output file
            - window: a tuple of the form (x1,x2,y1,y2) which indicates the 
                window to use. all numbers are inclusive
            - dim1Values: tuple of the form (start,stop,step) for the range that 
                defines dimension 1. 
            - dim2Values: tuple of the form (start, stop, step) for the range that 
                defines dimension 2
                *Note: The start and stop are written from left to right and 
                    from bottom to top
        '''

        #First find the window that we want to extract
        #We will create dummy numpy arrays to find out where to slice

        #dim1
        #np.arrange(start,stop,step)
        dim1Range = np.arange(dim1Values[0],dim1Values[1]+dim1Values[2],dim1Values[2])
        #Create dim 2
        dim2Range = np.arange(dim2Values[0],dim2Values[1]+dim2Values[2],dim2Values[2])
        #Now we can find the location of the window values

        #Now we can find the window values
        windowIndex = []
        for i,w in enumerate(window):
            #check if we are dealing with dim 1 or 2
            if i < len(window)/2:
                #Then we want to deal with dim1
                windowIndex.append(np.where(dim1Range == w)[0][0])
            elif i >= len(window)/2:
                #We want to deal with dim 2
                windowIndex.append(np.where(dim2Range == w)[0][0])
        if DEBUG:
            print("WindowIndex:",windowIndex)
        #Create an output dictionary
        winAvg = dict()
        #iterate through all of the conditions
        for cond in ['Anode','Cathode','Sham','Visual']:
            #Now we can iterate through all of the directories
            for path in directories:
                os.chdir(path)
                #We want to then iterate through all the files
                for f in os.listdir():
                    if not f.endswith('.tfc'):
                        #we don't want to read this so continue
                        continue
                    if not (cond.lower() in f.lower()):
                        continue#we will come back to this one
                    #we want to first load in the sources
                    if DEBUG:
                        print(f)
                    tfc = self.loadtfc(f)
                    try:
                        _ = winAvg[f.split('_')[0]]
                    except KeyError:
                        #If the key doesn't exist, we need to make a new entry
                        winAvg[f.split('_')[0]] = dict()
                    for source,arr in tfc.items():
                        #Find the avg
                        arr = arr.astype(float)
                        avg = arr[windowIndex[0]:windowIndex[1]+1,windowIndex[2]:windowIndex[3]+1].mean()
                        
                        #Save the avg
                        winAvg[f.split('_')[0]]["{}_{}".format(cond,source)] = avg

        #Now we can save the output file
        df = pd.DataFrame.from_dict(winAvg)
        df = df.transpose()
        #Now we can save it in the correct directory
        df.to_csv(os.path.join(outputDir,"eegWindowAvgs.csv"))






        

if __name__ == '__main__':

    eeg = EEGProcessing()
    
    '''###WRITE COMMANDS TO CHECK loadtfc
    #Cd into a directory to check the function
    directory = "/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/EEG Data/TSE paper2/Controls Source TSE/Anode1 and2" 
    for f in os.listdir(directory):
        if not f.endswith('.tfc'):
            #we dont care about this file so continue
            continue
        #call the function
        print(f)
        eeg.loadtfc(os.path.join(directory,f))
    '''
    controlDir = "/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/EEG Data/TSE paper2/Controls Source TSE"
    patientDir = "/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/EEG Data/TSE paper2/Patients Source TSE"

    #find all of the sub directories
    dirs = []
    for d in os.listdir(controlDir):
        dirs.append(os.path.join(controlDir,d))
    for d in os.listdir(patientDir):
        dirs.append(os.path.join(patientDir,d))

    #Make sure everything we have are directories, if not pop them from the list
    newDirs = dirs
    for i,d in enumerate(dirs):
        if not os.path.isdir(d):
            #pop it from the list
            newDirs.pop(i)

    dirs = newDirs
    outputDir = "/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/EEG Data/TSE paper2"
    #Now we can pass this into the 
    eeg.findWindowAvg(outputDir,directories=dirs,window=(18,12,-100,0),dim1Values=(50,4,-2),dim2Values=(-400,200,25))

            
