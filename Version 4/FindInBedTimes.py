""" Title: MotionWareSleepAnalysis 
    Purpose: To determine the sleep points and awake times from raw data and 
            sleep diaries for given.
    Author: Daniel Backhouse and Alan Yan
"""
import numpy as np

def find_in_bed_time(dates, time, activity, lux, window_size):
    """ Finds the got up and lights out times using only the activity, light
    and date arrays
    
    Based on the length of the activity (i.e. the number of days of activity 
    for which data was recorded). The find_in_bed_time function will find the
    in bed and got up times of the participant and return the two as a list.
    The length of the list will vary depending on the number of days and 
    the study period.
    
    :param (array) date: the dates over which activity and light were recorded
    :param (array) time: the times at which the activity and light were recorded
    :param (array) activity: the activity for the specified epochtime
    :param (array) lux: the lux for the specified epoch
    :param (int) window_size: the size in hours of the window to check for sleep
    windows
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)
    """
    sleep_window_indices = get_sleep_window_indices(activity,lux,time,window_size)
    lights_out_indices = list()
    got_up_indices = list()
    lights_out_dates = list()
    lights_out_times = list()
    got_up_times = list()
    got_up_dates = list()
    for index in sleep_window_indices:
        sleep_range_backward = index - 2*60
        sleep_range_forward = index + 3*60 
        lights_out_index = find_lights_out_index(sleep_range_backward, activity,
                                                 lux, sleep_range_forward )    
        lights_out_indices.append(lights_out_index)
        
        start = index
        end = index + window_size*60
        sleepRangeMean = np.mean(activity[start:end])
        awake_range_backward = index + 3*60
        awake_range_forward = index + 9*60
        got_up_index = find_got_up_index(awake_range_backward, activity, lux, 
                                         awake_range_forward, sleepRangeMean )
        got_up_indices.append(got_up_index)
        
        lights_out_times.append(time[lights_out_index])
        lights_out_dates.append(dates[lights_out_index])
        got_up_times.append(time[got_up_index])
        got_up_dates.append(dates[got_up_index])
    
    return lights_out_dates, lights_out_times, got_up_dates, got_up_times

#TODO: Write docstring
def get_sleep_window_indices(activity, lux, time, window_size):
    """ Gets the sleep window indices
    """
    days_of_recorded_activity = int(len(activity)/1440)
    print(days_of_recorded_activity)
    start_index = find_start_index(time)
    days_indices = get_day_indices(start_index, days_of_recorded_activity)
    
    sleep_window_indices = list()
    for i in range(0, len(days_indices)-1):
        start = days_indices[i]
        end = days_indices[i+1]        
        sleep_window_index = find_sleep_window(activity[start:end], lux[start:end], window_size)
        sleep_index = start + sleep_window_index
        sleep_window_indices.append(sleep_index)
    
    # Get from last index to end of raw data file
    print(len(sleep_window_indices))
    return sleep_window_indices
    
def find_sleep_window(activity, lux, size):
    """ Finds and returns all windows of given size within the date, time, acitivty
    and lux data given
    
    :param (array) activity: 24 hour activity data taken from participant
    :param (int) size: size given in hours for the sleep range
    :return: the index corresponding to the start of the mopst likely
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
        
    sortedIndex = sort_lists(light_list, activity_list, index_list)
    sleep_index  = sortedIndex[len(sortedIndex)-1]   
    return  sleep_index
     
def find_start_index(time):
    """ Find the first 12th hour in the time list and returns its index
    
    :param (array) time: a list of datetime.time objects
    :raises: raises an exception if there was no 12pm hour found
    :return: returns the first 12pm time
    :rtype: (int)
    """    
    for index in range(0,len(time)):
        if(time[index].hour == 12):
            return index
    
    raise Exception('did not find any 12pm value within the entire time array')
        
def get_day_indices(start_index, worn_days):
    """Gets the indices for the start of each day begining at 12pm for the 
    duration of the study
    
    :param (int) start_index: the first 12pm time index
    :param (double) worn_days: the number of proper data worn days
    return: A list of the indices which correspond to a time of 12pm
    :rtype: list<int>
    """
    day = 1440
    start_day_indices = list()
    index = start_index
    while index <= worn_days*day:
        start_day_indices.append(index)
        index = index + day
    
    return start_day_indices
    
# TODO: complete docstring   
def sort_lists(lightList, activityList, indexRangeList):
    """ Sorts the lightList by the windows with the least amount of zero light counts
    first and sorts the activityList by the windows with the most counts below the mean
    
    :param (list) lightList: takes a list of sleep windows with lux data
    :param(list) activityList: takes a list of sleep windows with activity data
    :param(list) indexRangelist: takes a list of the indices corresponding to
    the activity and light data points
    """
    activityThreshold = 20
    lightWeight = 1
    activityWeight = 1
    weightedSleepPeriods = list()
    for i in range(0 , len(activityList)):
        activityVal =  count_below_threshold_in_array(activityList[i], activityThreshold)
        lightVal = count_zeros_in_array(lightList[i])
        val = activityVal*activityWeight + lightWeight*lightVal
        weightedSleepPeriods.append(val)
    
    sortedIndexRange = bubbleSort(weightedSleepPeriods, indexRangeList)
    
    return sortedIndexRange

def bubbleSort(arr, arr2): 
    """ Bubble sorts array1 and moves the elements in arr2 in the same manner 
    as array1 indpenedent of the size the elements within it
    
    :param (array<int>) arr: an array of integers
    :param (array<int>) arr2: an array of any data type
    :return: returns array 2 sorted using array 1
    """
    n = len(arr) 
  
    for i in range(n): 
        for j in range(0, n-i-1): 
            if arr[j] > arr[j+1] : 
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]
    return arr2

def count_below_threshold_in_array(arr, threshold):
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

def count_zeros_in_array(arr):
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

def find_lights_out_index(index, activity, lux, sleepRange):
    """ Finds the lights out time of the participant given activity sleep range
    and lux sleep range
    
    :param (array) activity: the activity data of the participant over a sleep range
    :param (array) lux: the lux data of the participant over the sleep range
    :return: the index corresponding to the moment the participant went to sleep
    """
    meanActivity = 20
    zeroMovementCount = 0;
    zeroLightCount = 0;
    zeroLightActiveCount = 0;
    darkMotion = 0;
    sleepActiveCheck = False
    sleepLightCheck = False
    lights_out_index = index   #Intialize lights out time
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
                      
                if activity[index] <= meanActivity:
                    darkMotion = darkMotion + 1;            
                
                if sleepLightCheck == False:
                    sleepLightCheck = True
                    lights_out_index = index  
            else:
                zeroLightCount = 0
                sleepLightCheck = False
                darkMotion = 0

            if darkMotion >= 5:  
                return lights_out_index
                  
            if zeroLightActiveCount >= 5:
                return lights_out_index
                    
            if zeroMovementCount >= 20:
                return lights_out_index
                  
            if zeroLightCount >= 15:
                return lights_out_index
            
            index = index + 1
                      
    return lights_out_index
    
def find_got_up_index(index, activity, lux, sleep_range, sleepRangeMean):
    """ Finds the got up time of the participant
    
    :param (array) activity: the activity data of the participant over a sleep range
    :param (array) lux: the lux data of the participant over the sleep range
    :param (int) sleep_range: the index corresponding to the end of the passed
        sleep range
    :param (double) sleepRangeMean: mean activity count over estimated sleep range
    :return: the index corresponding to the moment the participant went to sleep
    :rtype: (int)
    """
    zeroStirringCount = 0;
    got_up_index = index
    
    while index < sleep_range:

        if lux[index] != 0 and activity[index] >= sleepRangeMean:
            zeroStirringCount = zeroStirringCount + 1
            if zeroStirringCount == 1:
                got_up_index = index               
        else:
            zeroStirringCount = 0
            
        if zeroStirringCount >= 10:
            return got_up_index
            
        index = index + 1
                 
             
    return got_up_index