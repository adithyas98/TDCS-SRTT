#!/usr/bin/env python3
import pandas as pd
import os
import itertools 
import numpy as np
#Created By Adithya Shastry
#Email: ams2590@cumc.columbia.edu
DEBUG = True

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
        #uniqueCondGroup = self.getUnique(self.originalDataFilepath,columns=['GROUP','CONDITION'])
        conditions = ['Anod','cath','vertex','sham']
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
                    if (c.lower() in f.lower()) and (g.lower() in f.lower()):
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
                outputDf['GroupSEMLogRT'] = outputDf.sem(axis=1)
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
        conditions = ['Anod','cath','vertex','sham']
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
                    if (c.lower() in f.lower()) and (g.lower() in f.lower()):
                        #open the file as a dataframe
                        tempDf = pd.read_csv(os.path.join(subjectFolder,f))

                        #now we can add a column
                        averageDf[f.split('.')[0]] = tempDf['PercentFast']
                #Save the file
                averageDf['GroupAvgPercentFast'] = averageDf.mean(axis=1,numeric_only=True)
                averageDf.to_csv(os.path.join(exportDir,"{}_{}_GroupAverages.csv".format(c,g)))

    def combineRTData(self,nonNormData,normData,outputDir):
        '''
        This function will combine and average the subject run data and output
        columns for the following:
            - Block 1
            - Block 2
            - Block 3
            - Random Trials from Block 1 and Block 2
            - Random Trials from Block 3
            - Average accross Block 1 and 2
        All of the above will be done for each of the conditions
        Inputs:
            - nonNormData:full filepath to the directory where the 
                nonNormData excel file is kept
            - normData: full filepath to the directory where the normalized
                data is kept
            - outputDir: Full filepath to where the output file should be
        '''
        #To comeplete this we first need to ensure that subject, run
        #   data is generated for both the nonNormData and normData
        for d in [nonNormData,normData]:
            uniqueValues = self.getUnique(filepath=d)
            try:
                self.averageTrials(filepath=os.path.join(d,'WrangledData','SUBJECT_RUN'))
            except:
                self.averageTrials(filepath=os.path.join(d,'NormalizedWrangledData','SUBJECT_RUN'))
        #Now we can look into averaging the data that we want
        conditions = self.getUnique(filepath=nonNormData,columns=['CONDITION'])[0]
        conditions = ['Vertex','Sham','Anod','Cath']
        subjects = self.getUnique(filepath=nonNormData)[0]
        
        #First create paths for where the subject,run average data
        #   is stored for each participant
        normalizedAvgData = os.path.join(normData,'NormalizedWrangledData','SUBJECT_RUN','subjectRunAvgs')
        nonNormalizedAvgData = os.path.join(nonNormData,'WrangledData','SUBJECT_RUN','subjectRunAvgs')
        #now we can create a dictionary to store our results

        rtSubjectData = dict()
        #Now we can iterate through each of the conditions,subjects
        for sub in subjects:
            #Here we want to create a new dictionary for the subject
            #We only want the subject code which is before the first "_"
            sub = sub.split("_")[0]
            rtSubjectData[sub] = dict()
            for cond in conditions:
                if DEBUG:
                    print(sub,cond)
                #We want to iterate through each condition since we have to compile
                #   all of the data points we want for each of the conditions
                
                #First deal with all of the normalized_data
                #Load up the excel file with run averages
                for f in os.listdir(normalizedAvgData):
                    if not (f.endswith('.csv') and (sub.lower() in f.lower()) and (cond.lower() in f.lower())):
                        #This isn't the file we are looking for so continue
                        continue
                    #Otherwise, we want to extract the information we want
                    if DEBUG:
                        print("Found 1")
                    df = pd.read_csv(os.path.join(normalizedAvgData,f))
                    
                    #Now we want to copy over the averageLogRt column
                    
                    for b,block in enumerate(np.array_split(df['AverageLogRT'],3)):
                         #First we want to take the average of the block
                         assert len(block) == 10#just to double check
                         avg = np.mean(block)
                         rtSubjectData[sub]["AvgNormLogRT{}Block{}".format(cond,b+1)] = avg

                    #Now, while we are here we should also average block 1 & 2
                    b1Avg = rtSubjectData[sub]["AvgNormLogRT{}Block{}".format(cond,1)]
                    b2Avg = rtSubjectData[sub]["AvgNormLogRT{}Block{}".format(cond,2)]

                    #Now we can average these and add them to the dict
                    rtSubjectData[sub]["AvgNormLogRT{}Block1_2".format(cond)] = (b1Avg + b2Avg)/2


                    #Now we can extract the random trial averages from the 
                    #   Non-normalized data
                    for f in os.listdir(nonNormalizedAvgData):
                        if not (f.endswith('.csv') and (sub.lower() in f.lower()) and (cond.lower() in f.lower())):
                            #This isn't the file we are looking for so continue
                            continue
                        if DEBUG:
                            print("Found 2")
                        #Load in the dataset
                        df = pd.read_csv(os.path.join(nonNormalizedAvgData,f))
                        for b,block in enumerate(np.array_split(df['AverageLogRT'],3)):
                            assert len(block) == 12#double check we are opening the right file
                            block = list(block)
                            avg = (block[0] + block[9])/2#The random runs are: 1,10
                            #The random trials are 1,10 in each block(12 runs)
                            rtSubjectData[sub]["AvgRandomLogRT{}Block{}".format(cond,b+1)] = avg

                        #we want to also get an avg for block 1 & 2
       

                        b1Avg = rtSubjectData[sub]["AvgRandomLogRT{}Block{}".format(cond,1)]
                        b2Avg = rtSubjectData[sub]["AvgRandomLogRT{}Block{}".format(cond,2)]

                        #Now we can average these and add them to the dict
                        rtSubjectData[sub]["AvgRandomLogRT{}Block1_2".format(cond)] = (b1Avg + b2Avg)/2
                
        #Now we can save our dictionary as a csv file
        df = pd.DataFrame(rtSubjectData)
        df = df.transpose()
        #Now we can save it
        df.to_csv(os.path.join(outputDir,'SubjectRTAvgs.csv'))



                    
                    

                    
            





        





if __name__ == '__main__':
    
    expG = ExponentialGraphs()

    ''' #Non-Normalized Data    
    fileDir = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data'
    uniqueValues = expG.getUnique(filepath=fileDir)

    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN/subjectRunAvgs')

    '''
    #Normalized Data

    expG = ExponentialGraphs()
    fileDir = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData'
    uniqueValues = expG.getUnique(filepath=fileDir)
    expG.averageTrials(filepath='/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN')

    expG.getGroupAvearges(filepath='/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs')

    subjectFolder = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs'
    trialDataFolder = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN'
    outputFolder = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData/NormalizedWrangledData/SUBJECT_RUN/subjectRunAvgs/groupAverageLogRTs'
    expG.percentFast(subjectFolder=subjectFolder,trialDataFolder=trialDataFolder,outputFolder=outputFolder,fastCutOff=-0.275)

    #combine and save RT data
    nonNormData = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data'

    normData = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData'
    outputDir = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data'


    expG.combineRTData(nonNormData,normData,outputDir)






