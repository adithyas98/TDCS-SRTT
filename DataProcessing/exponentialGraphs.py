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

    def percentFast(self,subjectFolder='',trialDataFolder='',outputFolder='',fastCutOff=-0.275):
        '''
        Finds the percent fast for each run of every subject. It takes into 
        account the individual trial data for each run for a given subject
        Inputs:
            -subjectFolder: Where the subject run level data is held
            -trialDatafolder: Where the trial level data is kept
            -outputFolder:Where to put the compiled group data
            -fastCutOff: The cutoff to determine if a reaction time is fast
        Output:
            -a folder that contains the group percent fast averages
            -a column in the subject level data that says the percent fast
                for each subject
        '''

        #load up the trial by trial data
        os.chdir(trialDataFolder)
        #get the unique subjects and runs

        uniqueSubjectRun = self.getUnique(self.originalDataFilepath,columns=['SUBJECT','RUN'])

        for subject in uniqueSubjectRun[0]:
            percentFast = []#hold percent fast data per run
            for run in uniqueSubjectRun[1]:
                #iterate through the file names and check to see if the run
                #   and subject name matches
                for f in os.listdir(trialDataFolder):
                    if (subject in f) and ("{}.csv".format(run) in f):
                        #then we have a match and can write if the trial was fast
                        #load the csv
                        df = pd.read_csv(os.path.join(trialDataFolder,f))
                        try:
                            df['Fast'] = df['LOG_RT'] <= fastCutOff
                        except:
                            #This is what the normalized dataset uses
                            df['Fast'] = df['Normalized_Log_RT'] <= fastCutOff
                        #Get the percent fast data and add it to the 
                        try:
                            percentFast.append(100*sum(df['Fast']==True)/(len(df['Fast'] + 1e-8)))
                        except:
                            percentFast.append(None)
                            print("Empty dataframe: {}".format(f))
                        #Now we can save the file
                        df.to_csv(os.path.join(trialDataFolder,f))
            for f in os.listdir(subjectFolder):
                if subject in f:
                    #then we can add our percent fast data
                    df = pd.read_csv(os.path.join(subjectFolder,f))
                    df['PercentFast'] = percentFast
                    df.to_csv(os.path.join(subjectFolder,f))
        #Create group average percent fast sheets
        #create a list to keep track of conditions
        conditions = ['Sham','Anod','Cath','Vertex']
        #create a list to deliniate subject groups
        groups = ['CONTROL','PATIENT']
        
        #change directory to the output
        os.chdir(outputFolder)
        #We can make another folder here to put the sheets
        exportDir = os.path.join(outputFolder,'PercentFastGroupAverages')
        if not (os.path.exists('PercentFastGroupAverages')):
            os.mkdir(exportDir)

        #iterate through each of the conditions and groups 
        # find all the subject average files that apply
        # then combine them into one file
        
        #get the unique runs first

        uniqueSubjectRun = self.getUnique(self.originalDataFilepath,columns=['RUN'])
        for c in conditions:
            for g in groups:
                #Make a data frame to store this data
                averageDf = pd.DataFrame()
                averageDf['RUN'] = uniqueSubjectRun[0]
                #Now iterate through the files and find the ones that match
                for f in os.listdir(subjectFolder):
                    if (c in f) and (g in f):
                        #open the file as a dataframe
                        tempDf = pd.read_csv(os.path.join(subjectFolder,f))

                        #now we can add a column
                        averageDf[f.split('.')[0]] = tempDf['PercentFast']
                #Save the file
                averageDf['GroupAvgPercentFast'] = averageDf.mean(axis=1,numeric_only=True)
                averageDf.to_csv(os.path.join(exportDir,"{}_{}_GroupAverages.csv".format(c,g)))


                    
            





        





if __name__ == '__main__':

    expG = ExponentialGraphs()

    '''#Non-Normalized Data    
    fileDir = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data'
    uniqueValues = expG.getUnique(filepath=fileDir)

    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN/subjectRunAvgs')
    '''


    #Normalized Data

    expG = ExponentialGraphs()
    fileDir = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData'
    uniqueValues = expG.getUnique(filepath=fileDir)

    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs')

    subjectFolder = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs'
    trialDataFolder = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN'
    outputFolder = '/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs/groupAverageLogRTs'
    expG.percentFast(subjectFolder=subjectFolder,trialDataFolder=trialDataFolder,outputFolder=outputFolder,fastCutOff=-0.275)




