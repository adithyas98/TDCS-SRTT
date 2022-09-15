#!/usr/bin/env python3
import pandas as pd
import os
import itertools 
#Created By Adithya Shastry
#Email: ams2590@cumc.columbia.edu


class ExponentialGraphs:

    def __init__(self):
        pass

    def getUnique(self,filepath='',columns=['SUBJECT','RUN']):
        '''
        Will find the unique values in any column asked
        input:
            -filepath: the filepath to the data
            -columns: list of columns to return unique values for
        returns:
            - a 2d array of unique values in the same order as columns 
                have been listed in the columns variable
        '''
        self.originalDataFilepath = filepath
        #change directory to the filepath
        os.chdir(filepath)
        dataFrames = []
        for f in os.listdir():
            if f.endswith('.xlsx'):
                dataFrames.append(pd.read_excel(f))

        #Now, we can concatenate a dataframe with all the data
        self.mainDF = pd.concat(dataFrames,axis=0)

        assert isinstance(columns,list)

        uniqueValues = []
        for c in columns:
            uniqueValues.append(list(self.mainDF[c].unique()))


        return uniqueValues

    def averageTrials(self,filepath=''):
        '''
        Will average the trials per run for every subject
        Inputs:
            - filepath: the filepath to the directory containing all of the data
        outputs:
            - csv files that save the average logRT for each run for a subject
        '''

        os.chdir(filepath)

        outputDir = os.path.join(filepath,'subjectRunAvgs')
        print(outputDir)
        if not os.path.exists(outputDir):
            #make the directory
            os.mkdir(outputDir)

        #get the unique values of subjects and runs

        uniqueSubjectRun = self.getUnique(self.originalDataFilepath,columns=['SUBJECT','RUN'])
        print(uniqueSubjectRun[0])

        for subject in uniqueSubjectRun[0]:
            averageRunDict = dict()
            averageRunDict['RUN'] = []#to hold the runs
            averageRunDict['AverageLogRT'] = []#to hold the average Log_RT
            for run in uniqueSubjectRun[1]:
                #now, we need to iterate through each of the subjects's runs
                #   create a single data frame for each subject
                for f in os.listdir(filepath):
                    if (subject in f) and ("{}.csv".format(run) in f):
                        df = pd.read_csv(os.path.join(filepath,f))
                        averageRunDict['RUN'].append(run)
                        try:
                            averageRunDict['AverageLogRT'].append(df['LOG_RT'].mean())
                        except:
                            #This is what the normalized dataset uses
                            averageRunDict['AverageLogRT'].append(df['Normalized_Log_RT'].mean())
            #We have procesed all of the runs, now we can save the files
            df = pd.DataFrame.from_dict(averageRunDict)

            #Save the dataframe
            outputPath = os.path.join(outputDir,"{}_AveargeRunLogRTs.csv".format(subject))
            df.to_csv(outputPath)
    def getGroupAvearges(self,filepath=''):
        '''
        Will get the group averages accross each run. 
        Inputs:
            - filepath: file path to where the subject level data is stored
        output:
            - csv files for each of the groups with their average run LogRTs
        '''

        #change directory into the filepath
        os.chdir(filepath)
        outputDir = os.path.join(filepath,'groupAverageLogRTs')
        print(outputDir)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        #create a list to keep track of conditions
        conditions = ['Sham','Anod','Cath','Vertex']
        #create a list to deliniate subject groups
        groups = ['CONTROL','PATIENT']
        #get the unique runs
        runs = self.getUnique(self.originalDataFilepath,columns=['RUN'])
        for c in conditions:
            for g in groups:
                print(c,g)
                #create a dictionary to hold values
                outputDict = dict()
                
                #now iterate through each of the files to find the ones that
                #   and append the ones that belong together
                for f in os.listdir(filepath):
                    if (c in f) and (g in f):
                        #then we want to add the subject to our dictionary
                        #first read the file
                        dataFile = pd.read_csv(os.path.join(filepath,f))
                        outputDict[f.split('.')[0]] = dataFile['AverageLogRT'].values
                        print(len(dataFile['AverageLogRT'].values),len(runs[0]))
                #save the dictionary as a csv
                outputDf = pd.DataFrame.from_dict(outputDict,orient='index')
                outputDf = outputDf.transpose()
                print(outputDf.head(10))
                #Now average subjects accross the runs
                outputDf['GroupAvgLogRT'] = outputDf.mean(axis=1)
                #then actually save it
                outputFilePath = os.path.join(outputDir,'{}_{}_RunAvgLogRT.csv'.format(c,g))
                outputDf.to_csv(outputFilePath)

    def percentFast(self,subjectFolder='',trialDataFolder=''):
        '''
        TODO: Create a percent fast column on all of the individual run results
            spreadsheets. Using the individual trial data spreadsheets
        '''


        





if __name__ == '__main__':

    expG = ExponentialGraphs()

    '''#Non-Normalized Data    
    fileDir = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data'
    uniqueValues = expG.getUnique(filepath=fileDir)

    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN/subjectRunAvgs')
    '''


    #Normalized Data
    fileDir = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData'
    uniqueValues = expG.getUnique(filepath=fileDir)

    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs')





