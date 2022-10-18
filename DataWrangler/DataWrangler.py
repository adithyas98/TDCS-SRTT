#!/usr/bin/env python3
import pandas as pd
import os
import itertools 
#Created By Adithya Shastry
#Email: ams2590@cumc.columbia.edu

DEBUG = True
class TDCSSRTTDataWrangler:
    '''
    This class will help format and separate data points so that they can be 
    used for further analysis
    '''
    def __init__(self,fileDir=None):
        '''
        Inputs:
            -fileDir: The directory where the excel files with raw data will 
               be held
        '''
        self.fileDir = fileDir
        #Now we can change the directory to this one
        os.chdir(self.fileDir)
        #Now, we can load up the files as a list of pandas data frames
        self.files = []
        if DEBUG:
            print(os.listdir(fileDir))
        for f in os.listdir(fileDir):
            if f.endswith('.xlsx'):
                self.files.append(f)
        #now open them as data frames
        self.dataFrames = []
        for f in self.files:
            self.dataFrames.append(pd.read_excel(f))
        if DEBUG:
            print(len(self.dataFrames))
            for data in self.dataFrames:
                print(data.head(10))
                print("-------------\n")

    def extractDataPoints(self,columns,labelCombinations=None,dataColumn=None):
        '''
        This method will extract the rows that we want to look at for specific 
        data points that are looking for based on the combinations we are 
        interested in. The method will take the columns we are interested in 
        isolating, find the unique values in that column, then it will iterate 
        through every combination of values for those columns and extract the 
        values that meet those conditions and store them as a dataframe
        Inputs:
            -columns (list of Strings): The columns that we are intereted in 
                looking at. *required
            -labelCombinations (list of Tuples):Specific label combinations 
                we want to look at. If the value is none, then we will simply
                find all of the possible values and created combinations out of
                them. The order of the tuples is determined by the order of 
                the column names passed in the columns parameter
            -dataColumn (list of Strings):The specific data columns that 
                we want to extract. If the value is left as None, then all 
                columns will be extracted-taking into account the 
                conditions of course!
            -
        Outputs:
            -Depends on what is passed into the dataColumn input parameter:
                -if None, then a dictionary with the column values as a key
                and their respective data frames as values
                -if a column is passed through,then the function will create
                a data frame with just those values along with descriptive
                column names
        '''
        #We just want to make sure we have the columns we are looking for
        for c in columns:
            for d in self.dataFrames:
                assert c in d.columns

        #Now we want to ensure that the label combinations exist in the columns
        if labelCombinations != None:
            for d in self.dataFrames:
                for i,col in enumerate(columns):
                    for l in labelCombinations[i]:
                        assert l in d[col].unique()
        #Now that we have checked everything, we can extract data
        #first contatenate the pandas dataframes that we have in our list
        self.mainDF = pd.concat(self.dataFrames,axis=0)
        if DEBUG:
            print("Head\n")
            print(self.mainDF.head(20))
            print("------------------\n")
            print("Tail\n")
            print(self.mainDF.tail(10))
        #Now that we have a concatenated data frame, we can now find the values
        #   we want to look to use as conditions
        columnConditions = []
        if labelCombinations != None:
            columnConditions = labelCombinations
        else:
            #If we dont have this then we will need to figure out all the unique
            #   values in each column
            for col in columns:
                columnConditions.append(self.mainDF[col].unique())

        #Now that we have this we can pass it into our combination function
        #   We are going to use itertools for this task
        columnCombinations = list(itertools.product(*columnConditions))

        #With this now we can iterate through each column combination and 
        #   pare down our data set after each successive iteration
        #we will now start using the dataColumn variable so see if it exists
        #   in the dataset
        if dataColumn != None:
            for d in dataColumn:
                assert d in self.mainDF.columns
        #Now we will need to modify our output based on the value
        if dataColumn != None:
            #then our output is a data frame
            extractedData = pd.DataFrame()
        else:
            #if this is not the case then we will create multiple dataframes
            #    and so we need a way to store them, we will use a dictionary
            extractedData = dict()
        for combination in columnCombinations:
            #We want to iterate through all of the conditions we want
            #   Each of the rows to meet and then create one final data frame
            df = self.mainDF.copy()
            for value,col in zip(combination,columns):
                df = df.loc[df[col] == value]
            if DEBUG:
                print("COMBINATION STEP")
                print(combination)
                print(df.head(50))
            #Now we can worry about saving everything correctly
            if dataColumn != None:
                #Then we will extract the columns we want and use descriptive names
                for d in dataColumn:
                    columnName = "{}_{}".format("_".join(combination),d)
                    #add the column in the data frame
                    extractedData[columnName] = df[d]
            else:
                #if dataColumn is None, then add it to a dictionary
                key = "_".join(combination)
                extractedData[key] = df

        return extractedData

            
    def combineData(self,directory,dataColumn):
        '''
        This method will combine all of the extracted data files
        and put the data into one dataFrame by column
        Inputs:
            -directory: the directory to check
            -datacolumn:the column to use for data
        '''
        combinedDataFrame = pd.DataFrame()

        #change directory into the directory above
        os.chdir(directory)
        for f in os.listdir():
            #check if the file is a csv
            if not f.endswith('.csv'):
                continue
            #Open up the data as a pandas dataframe
            fileData = pd.read_csv(f)
            if DEBUG:
                print(fileData.head())
            combinedDataFrame[f.split('.')[0]] = fileData[dataColumn]
        return combinedDataFrame

    def saveDataFrame(self,data,directory,baseFilename=''):
        '''
        This method will save the data frame or dictionary
        Inputs:
            - data (dictionary or dataframe): This is the data that we want
                to save as a excel file. This function plays well with the 
                extractDataPoints method above.
            - directory: the directory to save the file in
            -baseFilename: The base name of the file. If data is a dictionary,
                the specific descriptors for the data frames in that 
                dictionary (the column names) will be added to this string. If
                data is a dataframe, then only this name will be used
        output:
            -None, just a saved file
        '''
        #First make the output directory if it doesn't exist
        if not os.path.exists(directory):
            os.mkdir(directory)
        os.chdir(directory)
        #Save the files based on if data is a dict or a dataframe
        if type(data) == dict:
            #Then we want to iterate through all of the keys and then
            #   Save the dataframe with that name
            print("Printing KEYS")
            print(data.keys())
            for key in data.keys():
                filename = "{}_{}".format(baseFilename,key)
                data[key].to_csv("{}.csv".format(filename))
        elif isinstance(data,pd.DataFrame):
            #We just want to save the dataframe with the basefilename
            data.to_csv("{}.csv".format(baseFilename))


if __name__ == '__main__':
    #fileDir = '/mnt/h/tDCS paper2 SRTT'
    #Non Normalized Data
    fileDir = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data'
    DW = TDCSSRTTDataWrangler(fileDir=fileDir)

    #Now we can create an output file
    outputDir = os.path.join(fileDir,'WrangledData')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    os.chdir(outputDir)

    

    '''
    #Columns 1
    columns = ['GROUP','BLOCK','TASK','CONDITION']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)

    #Columns 2
    columns = ['GROUP','TASK']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)

    #Columns 3
    columns = ['SUBJECT','RUN']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)   


    print("Combining Data!")
    #Now we can go through and create the combined csv files
    os.chdir(outputDir) 
    for d in os.listdir():
        if not os.path.isdir(d):
            #Not a directory so continue
            continue
        folder = os.path.join(outputDir,d)
        extractedData = DW.combineData(folder,'LOG_RT')
        DW.saveDataFrame(extractedData,folder,baseFilename="{}_CombinedData".format(d))

    
    #Columns 1,Log RT Only
    columns = ['GROUP','BLOCK','TASK','CONDITION']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns,dataColumn=['LOG_RT'])
    DW.saveDataFrame(extractedData,folder,"{}_LOG_RTs".format(folder))
    os.chdir(outputDir)


    print("Combining Data!")
    #Now we can go through and create the combined csv files
    os.chdir("/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN/subjectRunAvgs") 
    folder = "/Users/adish/Documents/NYPSI and NKI Research/TDCS-SRTT/data/WrangledData/SUBJECT_RUN/subjectRunAvgs"
    extractedData = DW.combineData(folder,'AverageLogRT')
    DW.saveDataFrame(extractedData,folder,baseFilename="{}_CombinedData".format("AverageRunRTbySubject&Condition"))
    '''


    #Run the same stuff for the normalized Data
    fileDir = '/Users/adish/Documents/NYPSI Research/TDCS-SRTT/data/NormalizedData'
    DW = TDCSSRTTDataWrangler(fileDir=fileDir)

    #Now we can create an output file
    outputDir = os.path.join(fileDir,'NormalizedWrangledData')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    os.chdir(outputDir)

    '''
    #Columns 1
    columns = ['GROUP','BLOCK','TASK','CONDITION']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)

    #Columns 2
    columns = ['GROUP','TASK']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)

    '''
    #Columns 3
    columns = ['SUBJECT','RUN']
    folder = '_'.join(columns)
    extractedData = DW.extractDataPoints(columns)
    print(type(extractedData))
    DW.saveDataFrame(extractedData,folder)
    os.chdir(outputDir)   

    '''
    print("Combining Data!")
    #Now we can go through and create the combined csv files
    os.chdir(outputDir) 
    for d in os.listdir():
        if not os.path.isdir(d):
            continue
        folder = os.path.join(outputDir,d)
        extractedData = DW.combineData(folder,'Normalized_Log_RT')
        DW.saveDataFrame(extractedData,folder,baseFilename="{}_CombinedData".format(d))
    '''
