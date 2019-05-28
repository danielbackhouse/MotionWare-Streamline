# Module: find_in_bed_times.py
# Purpose: This module is used to find the Got Up and Lights Out times 
# of participant using the datetime, activity and lux data of said participant.
# Authors: Daniel Backhouse and Alan Yan

import numpy as np
import datetime
import time
#TODO: Modify docstring to once sleep analysis is completed
def find_in_bed_time(dateTimes, activity, lux, window_size, dm, zmc, zac, zlc, ta):
    """ Finds the got up and lights out times of a participant
    
    ****NOTE: This module and corresponding program has ONLY been validated
    on CamNTech's Motion Watch 8 Actigraphs for:
        - 1 minute epoch length
        - unaxial measurment
        - light exposure set to on
    Therefore sleep analysis results can NOT be guaranteed for any other actigraph
    or subsequent settings.
    
    The program was validated on three studies (*see repository for more information
    on software validation).
    
    The find_in_bed_time function is the only function within the FindInBedTimes.py
    module intended to be public. It is important that the arrays sent to this
    function are formatted correctly else the function will NOT return the
    correct value. The arrays should each be formatted as follows:
        - dateTimes:
            - an array of datetime objects in chronological order
            with the oldest date as the first entry.
            - each procedding element in the array must contain a datetime
            object 1 minute ahead of the previous datetime element
        - activity:
            - an array of int datatypes containing the acitivity data
            from a uniaxial actigraph recorded for a one minute epoch length
            - each element in the array must share the index of its corresponding
            date and time within the datetime array
        - lux:
            - an array of int objects containing the light exposure data
            from a uniaxial actigraph recorded for a one minute epoch length
            - each element in the array must share the index of its corresponding
            date and time within the datetime array
    
    The function begins by searching for the index corresponding
    to the first 12pm time within the dateTimes array. It then segments the
    rest of the data into 24 hour segment starting and ending at 12pm and places
    them in a list. 
    
    Each 24 hour segment is then further broken down into all possible window_size 
    segments within the 24 hour period seperated by an hours length. 
    
    The window_size segments are then sorted based on the number of zero activity
    counts and zero light counts within that time period (added using some
    weights). The segment with the largest value is then selected and is 
    classified as the sleep range. 
    
    The sleep range is then sent to Light's Out algrithim and the Got Up 
    algorithim (these can be found in the main folder of the repository under
    the folder (sleep window algorithms)).
    
    The function then uses the Light's Out and Got Up times determined by
    their respective algorithms to execute the sleep analysis. Note here
    that all sleep analysis calculations have been done according to the 
    methods given in the MotionWare Software Manual which can also be found
    in this repository.
    
    The execution of this function relies on several private functions not 
    intended to be used outside of this module.
    
    :param (array) dateTime: the dates and times over which activity and light 
        were recorded
    :param (array) activity: the activity for the specified epoch length
    :param (array) lux: the lux for the specified epoch length
    :param (int) window_size: the size in hours of the window to check for sleep
    windows
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)
    :raises: Exception (no 12pm in array)
    """
    #TODO: Bug in __get_sleep_window indicies (BT 002 Final)
    sleep_window_indices = __get_sleep_window_indices(activity,lux,dateTimes,window_size)
    lights_out_indices = list()
    got_up_indices = list()
    lights_out_dateTimes = list()
    got_up_dateTimes = list()
    sleep_analysis_list = list()
    
    for index in sleep_window_indices:
        sleep_range_backward = index - 2*60
        sleep_range_forward = index + 3*60 
        lights_out_index = __find_lights_out_index(sleep_range_backward, activity,
                                                 lux, sleep_range_forward,
                                                 dm, zmc, zac, zlc, ta )    
        lights_out_indices.append(lights_out_index)
        
        start = index
        end = index + window_size*60
        sleepRangeMean = np.mean(activity[start:end])
        awake_range_backward = index + 3*60
        awake_range_forward = index + 9*60
        got_up_index = __find_got_up_index(awake_range_backward, activity, lux, 
                                         awake_range_forward, sleepRangeMean )
        got_up_indices.append(got_up_index)
        
        #TODO: Do something with the returned dictionary
        #sleepAnalysisInfo = SleepDataAnalysis.findSleepAnalysisData(activity[lights_out_index-10: got_up_index+11], 
        #                   dateTimes[lights_out_index: got_up_index+1])
        
        #sleep_analysis_list.append(sleepAnalysisInfo)
        lights_out_dateTimes.append(dateTimes[lights_out_index])
        got_up_dateTimes.append(dateTimes[got_up_index])
        
    return lights_out_dateTimes, got_up_dateTimes, sleep_analysis_list

def __get_sleep_window_indices(activity, lux, dateTimes, window_size):
    """ Gets the sleep window indices ( the sleep ranges of window_size)
    
    :param (array) dateTime: the dates and times over which activity and light 
        were recorded
    :param (array) activity: the activity for the specified epoch length
    :param (array) lux: the lux for the specified epoch length
    :param (int) window_size: the size in hours of the window to check for sleep
    windows
    :return: a list containing the indicies that each sleep window start at
    :rtype: (list)
    """
    days_of_recorded_activity = int(len(activity)/1440)
    start_index = __find_start_index(dateTimes)
    days_indices = __get_day_indices(start_index, days_of_recorded_activity)
    sleep_window_indices = list()
    for i in range(0, len(days_indices)-1):
        start = days_indices[i]
        end = days_indices[i+1]        
        sleep_window_index = __find_sleep_window(activity[start:end], lux[start:end], window_size)
        sleep_index = start + sleep_window_index
        sleep_window_indices.append(sleep_index)
    # window size has tob e plus 2 so that the got up guess does not exceed the index limit
    #TODO fix this ting
    if(dateTimes[days_indices[-1]] + datetime.timedelta(hours = window_size + 2) > dateTimes[-1]):
        print('dont add entry')
    if(days_indices[-1] + 24*60 >= len(dateTimes)):
        start = days_indices[-1]
        end = len(dateTimes) - 1
        last_index = __find_sleep_window(activity[start:end], lux[start:end], window_size)
        sleep_window_indices.append(start + last_index)
    else:
        start = days_indices[-1]
        end = start + 24*60
        last_index = __find_sleep_window(activity[start:end], lux[start:end], window_size)
        sleep_window_indices.append(start + last_index)
        
    return sleep_window_indices
    
def __find_sleep_window(activity, lux, size):
    """ Finds and returns all windows of given size within the date, time, acitivty
    and lux data given
    
    :param (array) activity: 24 hour activity data taken from participant
    :param (int) size: size given in hours for the sleep range (window_size)
    :return: the index corresponding to the start of the most likely
    sleep window within the given set of 24 hour activity data
    """
    one_hour_epoch = 60
    sleepRange = size*60  
    activity_list = list()
    light_list = list()
    index_list = list()
    index = 0
    while (index + sleepRange) <= len(activity):
        light_list.append(lux[index:index+sleepRange])
        activity_list.append(activity[index:index+sleepRange])
        index_list.append(index)
        index = index + one_hour_epoch
    
    activityThreshold = 20
    lightWeight = 1
    activityWeight = 1
    weightedSleepPeriods = list()
    for i in range(0 , len(activity_list)):
        activityVal =  __count_below_threshold_in_array(activity_list[i], activityThreshold)
        lightVal = __count_zeros_in_array(light_list[i])
        val = activityVal*activityWeight + lightWeight*lightVal
        weightedSleepPeriods.append(val)
    sleep_index  = max(range(len(weightedSleepPeriods)), key=weightedSleepPeriods.__getitem__)
    return  sleep_index
     
def __find_start_index(dateTimes):
    """ Find the first 12th hour in the time list and returns its index
    
    :param (array) time: a list of datetime objects
    :raises: raises an exception if there was no 12pm hour found
    :return: returns the first 12pm time
    :rtype: (int)
    """   
    for index in range(0,len(dateTimes)):
        if(dateTimes[index].hour == 12):
            return index
    raise Exception('did not find any 12pm value within the entire time array')
        
def __get_day_indices(start_index, worn_days):
    """Gets the indices for the start of each day begining at 12pm for the 
    duration of the study
    
    :param (int) start_index: the first 12pm time index
    :param (double) worn_days: the number of proper data worn days
    :return: A list of the indices which correspond to a time of 12pm
    :rtype: list<int>
    """
    day = 1440
    start_day_indices = list()
    index = start_index
    while index <= worn_days*day:
        start_day_indices.append(index)
        index = index + day
    
    return start_day_indices

def __count_below_threshold_in_array(arr, threshold):
    """ Counts the number of elements in array below threshold
    
    :param (array) arr: an array of int's
    :return: The number of elements in array below threshld
    :rtype: (int)
    """
    counter = 0;
    for num in  arr:
        if(num <= threshold):
            counter = counter + 1
            
    return counter

def __count_zeros_in_array(arr):
    """ Counts the number of zeros in an array with integer values
    
    :param (array) arr: an array of int's
    :return: The number of zeros in the array
    :rtype: (int)
    """
    zero_counter = 0;
    for num in  arr:
        if(num == 0):
            zero_counter = zero_counter + 1
            
    return zero_counter

def __find_lights_out_index(index, activity, lux, sleepRange, dm, zmc, zac, zlc, ta):
    """ Finds the lights out time of the participant given activity sleep range
    and lux sleep range
    
    :param (array) activity: the activity data of the participant
    :param (array) lux: the lux data of the participant 
    :param (int) index: the starting index of the sleep_range
    :param (int) sleepRange: the size of the sleep range (window_size)
    :return: the index corresponding to the moment the participant went to sleep
    """
    zeroMovementCount = 0;
    zeroLightCount = 0;
    zeroLightActiveCount = 0;
    darkMotion = 0;
    sleepActiveCheck = False
    sleepLightCheck = False
    lights_out_index = index
    while index <= sleepRange:       

            if activity[index] == 0:
                zeroMovementCount = zeroMovementCount + 1 
                      
                if lux[index] == 0:
                    zeroLightActiveCount = zeroLightActiveCount + 1     
                      
                if sleepActiveCheck == False:
                    sleepActiveCheck = True
                    lights_out_index = index  
            else:
                zeroMovementCount = 0
                sleepActiveCheck = False
                zeroLightActiveCount = 0
             
            if lux[index] == 0:
                zeroLightCount = zeroLightCount + 1
                      
                if activity[index] <= ta:
                    darkMotion = darkMotion + 1;            
                
                if sleepLightCheck == False:
                    sleepLightCheck = True
                    lights_out_index = index  
            else:
                zeroLightCount = 0
                sleepLightCheck = False
                darkMotion = 0
                
            if darkMotion >= dm:
                return lights_out_index
                  
            if zeroLightActiveCount >= zac:
                return lights_out_index
                    
            if zeroMovementCount >= zmc:
                return lights_out_index
                  
            if zeroLightCount >= zlc:
                return lights_out_index
            
            
            index = index + 1
                      
    return lights_out_index
    
def __find_got_up_index(index, activity, lux, sleep_range, sleepRangeMean):
    """ Finds the got up time of the participant
    
    :param (array) activity: the activity data of the participant
    :param (array) lux: the lux data of the participant
    :param (int) sleep_range: the index corresponding to the end of the passed
        sleep range
    :param (int) sleep_range: the size of the sleep range (window_size)
    :param (double) sleepRangeMean: mean activity count over estimated sleep range
    :return: the index corresponding to the moment the participant went to sleep
    :rtype: (int)
    """
    zeroStirringCount = 0;
    got_up_index = index 
    while index < sleep_range and index < len(activity): # added less than end of len activity                                                      
        if lux[index] != 0 and activity[index] >= sleepRangeMean: # so that if the last indice
            zeroStirringCount = zeroStirringCount + 1   # happens to be late we account for that
            if zeroStirringCount == 1:
                got_up_index = index               
        else:
            zeroStirringCount = 0
            
        if zeroStirringCount >= 10:
            return got_up_index
            
        index = index + 1
                       
    return got_up_index