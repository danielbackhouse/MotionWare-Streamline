""" Title:
    Purpose:
"""
#Import extension libraries
import os
import pandas as pd

#Directories for folder locations
rawDataDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data'
sleepDiaryDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Diary.xlsx'



def findMatching(fileName):
    """Finds the matching patient in the diary or the raw data files
    
    Takes in a file name, and gets the patient number from it. If the fileName 
    comes from a raw data sheet, it will look for the number in the sleep diary
    and if the fileName comes from the sleep diary, it will look for the 
    raw data file with that number. fileName MUST be formatted as specified in 
    the read me document.
    
    :param: fileName
    :return: Returns either True or False depending on if the number is found
    :rtype(boolean)
    """
    numbers = fileName[3:6]
    
    if fileName.endswith('.xlsx'):
        rawSleepDiary = pd.ExcelFile(sleepDiaryDirectory)
        for sheetName in rawSleepDiary.sheet_names:         
            if sheetName.find(numbers) == 3:
                return True
    else:
        rawDataAll = os.listdir(rawDataDirectory+ '\Baseline')
        for file in rawDataAll:
            if file.find(numbers) == 3:
                return True
    return False
    
def populateRawDataList():
    """Creates and populates a list containing all the trials raw data 
    in numerical order
    
    
    :param: none
    :return: list of all trials raw data
    :rtype(list)
    """
    rawDataList = []
    rawDataAll = os.listdir(rawDataDirectory+ '\Baseline')
    
    for file in rawDataAll:
        if file.endswith('.xlsx') and findMatching(file):
            rawDataList.append(pd.read_excel(rawDataDirectory + '\Baseline\\' + file))  
        
    return rawDataList

def populateDiaryList():
    """Creates and populates a list of all sleep diaries, in numerical order
        
    Looks at all         
    :param: none
    :return: list of all trials sleep diaries
    :rtype(list)
    """
    diaryList = []
    rawSleepDiary = pd.ExcelFile(sleepDiaryDirectory)
    
    for sheetName in rawSleepDiary.sheet_names:
        if findMatching(sheetName):
            diaryList.append(pd.read_excel(sleepDiaryDirectory, sheet_name = sheetName))
        
    return diaryList
            
"""
@Main: Runs the main
@Purpose: Runs each function to execute the program
"""
rawDataList = populateRawDataList()
diaryList = populateDiaryList()
diaryDataPairList = [rawDataList,diaryList]
print(len(rawDataList),len(diaryList))

#Testing, patient one would be diaryDataPairList[0][0] and diaryDataPairList[1][0]. etc
#print(diaryDataPairList[0][0])
#print(diaryDataPairList[1][0])
#print(diaryDataPairList[0][7])
#print(diaryDataPairList[1][7])
#print(diaryDataPairList[0][25])
#print(diaryDataPairList[1][25])
#print(diaryDataPairList[0][93])
#print(diaryDataPairList[1][93])
        