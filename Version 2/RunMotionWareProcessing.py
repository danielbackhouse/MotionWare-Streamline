""" Title: RunMotionWareProcessing
    Purpose: To run the sleep processing on a given dataset 
    Author: Daniel Backhouse and Alan Yan
"""

__license__ = "Daniel Backhouse"
__revision__ = " $Id: RunMotionWareProcessing.py $ "
__docformat__ = 'reStructuredText'


# Supress warnings message
import warnings; warnings.simplefilter("ignore");

# Import extenstion libraries
#TODO: Change title of this at some point
import MotionWareAnalysis
import SheetManager
import time

start = time.time()
rawDataList = SheetManager.populateRawDataList()
diaryList = SheetManager.populateDiaryList()
diaryDataPairList = [rawDataList,diaryList]
midway = time.time()
print("\n Found the data... \n")
print("\n Calculting sleep points for first participant... \n")

      
sleepTimes, awakeTimes = MotionWareAnalysis.findSleepPoint(diaryList[0], 
                                                           rawDataList[0])

end = time.time()
print("\n Completed. \n")
      

