#!/usr/bin/env python3
import pandas as pd
import os
import itertools 
from functools import partial
import numpy as np
#Created By Adithya Shastry
#Email: ams2590@cumc.columbia.edu

DEBUG = True
class ShortFatConverter:
    '''
    This will convert the long thin format of the coherence data 
    into the short-fat format.
    '''

    def __init__(self):
        pass
    def convert(self,file,outfile,includeGroup=False):
        '''
        This method will do the conversion necessary
        Inputs:
            -file: the full filepath to the file we want to convert
            -outfile: the full filepath with name of the file we want to 
                create
        '''
        df = pd.read_excel(file)#Read the excel file

        #Values to replace for the numerical
        connections = ['SMA-Motor','SMA-Visual','Motor-Visual']
        conditions = ['Sham','Anode','Cathode','Visual','Sham Baseline']
        groups = ['Control','Patient']

        #Change numerical values to the category names
        #Change connections
        change = partial(self.changeValues,values=connections,unique=df['Connection'].unique())
        df['Connection'] = df['Connection'].apply(change)
        #change conditions
        change = partial(self.changeValues,values=conditions,unique=df['Condition'].unique())
        df['Condition'] = df['Condition'].apply(change)
        #change groups
        #change = partial(self.changeValues,values=groups,unique=df['Group'].unique())
        #df['Group'] = df['Group'].apply(change) 

        #We want to get all of the unique values in the columns
        #Get a list of the subjects
        subjects = df['Subject'].unique()
        connections = df['Connection'].unique()
        #conditions = df['Condition'].unique()#This will include sham baseline
        conditions = ['Sham','Anode','Cathode','Visual','Sham Baseline']


        #The idea is to iterate through each of the subjects,conditions,connections
        #   and create an entry in a dictionary to then save
        output = {}#create an empty dict to store our data
        for sub in subjects:
            output[sub] = {}
            for conn in connections:
                for cond in conditions:
                    #Filter out the dataset so we find what we need
                    data = df[(df['Subject']==sub) & (df['Connection']==conn) & (df['Condition']==cond)] 
                    if DEBUG:
                        print(data.head())
                    if includeGroup:
                        try:
                            output[sub]["Group"] = int(data['Group'].values[0])
                        except IndexError:
                            if "Group" in output[sub]:
                                #If it has the key then we also want to check 
                                #   if the value is correct
                                if output[sub]["Group"] != '':
                                    #don't do anything to the current value
                                    pass
                                else:
                                    output[sub]["Group"] = ''
                    try:
                        output[sub]["{}_{}_Coherence".format(cond,conn)] = data['Coherence'].values[0]
                    except IndexError:
                        #We don't seem to have a value here so we will just leave blank
                        output[sub]["{}_{}_Coherence".format(cond,conn)] = ''


        #Now we can convert this into a df and save it
        outputDF = pd.DataFrame.from_dict(output)
        outputDF = outputDF.transpose()
        if DEBUG:
            print(outputDF.head())


        #Now we can save it 
        outputDF.to_csv(outfile)

                        

         
    def changeValues(self,x,values=None,unique=None):
        return values[np.where(unique==x)[0][0]]


       


if __name__ == '__main__':

    conv = ShortFatConverter()

    file = "Coherence results_controls and patients.xlsx"
    outfile = "{}_SHORTFAT.csv".format(file.split('.')[0])

    conv.convert(file,outfile)

    #Do the same conversion but with the group names
    outfile = "{}_SHORTFATwithGroupNames.csv".format(file.split('.')[0])
    
    conv.convert(file,outfile,includeGroup=True)

        
