""" Title: MotionWareSleepAnalysis 
    Purpose: To determine the sleep points and awake times from raw data and 
            sleep diaries for given.
    Author: Daniel Backhouse and Alan Yan
"""

def find_in_bed_time(dates, time, activity, lux, study_period, start_threshold, 
                     activity_sleep_window_threshold, light_sleep_window_threshold):
    """ Finds the got up and lights out times using only the activity, light
    and date arrays
    
    Based on the length of the activity (i.e. the number of days of activity 
    for which data was recorded). The find_in_bed_time function will find the
    in bed and got up times of the participant and return the two as a list.
    The length of the list will vary depending on the number of days and 
    the study period.
    
    :param (array) date: the dates over which activity and light were recorded
    :param (array) time: the times at which the activity and light were recorded
    :param (array) activity: the activity for the specified epoch
    :param (array) lux: the lux for the specified epoch
    :param (int) study_period: the number of days the sleep study was
        conducted over
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)
    """
    # Each epoch is 1 minute. There are 14440 minutes in a day.
    days_of_recorded_activity = len(activity)/1440
    
    if(len(dates) != len(activity)):
        print('Error length of dates does not match length of activity')
    
    # The raw data should be taken over a period of 14 days selected by the 
    # person ding the analysis. This checks to see of the total number of epochs is 
    # 20160 (14 days) or just length of the study period
    if(study_period == days_of_recorded_activity):
        LO, GU = get_in_bed_time_complete_activity(dates,time,activity,lux, study_period)
    
    if(study_period < days_of_recorded_activity):
        print('Raw actiivty data exceeds study time' )
        LO, GU = get_in_bed_time_large_activity(dates,time,activity,lux,
                                                study_period, start_threshold, 
                                                activity_sleep_window_threshold,
                                                light_sleep_window_threshold)
        
    if(study_period > days_of_recorded_activity):
        LO, GU = get_in_bed_time_small_activity(dates, time, activity, lux, study_period)
         



def get_in_bed_time_complete_activity(date, time, activity, lux, study_period):
    """ Finds the lights out and got up times of a participant where 
    the days for which acitivity was recorded is equal to the number
    of days the study was done over
    
    :param (array) time: the times at which the activity and light were recorded
    :param (array) activity: the activity for the specified epoch
    :param (array) lux: the lux for the specified epoch
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)  
    """  

def get_in_bed_time_large_activity(date, time, activity, lux, study_period, 
                                   start_threshold, activity_sleep_window_threshold,
                                   light_sleep_window_threshold):
    """ Finds the lights out and got up times of a participant where 
    the days for which acitivity was recorded exceeds  the number
    of days the study was done over
    
    :param (array) time: the times at which the activity and light were recorded
    :param (array) activity: the activity for the specified epoch
    :param (array) lux: the lux for the specified epoch
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)  
    """ 
    got_up_dates = []
    got_up_times = []
    lights_out_dates = []
    lights_out_times = []
    
    start_index = find_start_point(activity, study_period, start_threshold)
    index = start_index
    one_hour_epoch = 60
    sleepRange = one_hour_epoch*12
    required_epoch_range = study_period*24*60
    
    while (index + sleepRange) <= (start_index + required_epoch_range):
        activity_zeros = count_zeros_in_array(activity)                 #light_zeros = count_zeros_in_array(lux)
        if(activity_zeros < activity_sleep_window_threshold):           #TODO: maybe check light
            lights_out_index = find_lights_out_index(
                    activity[index: index+sleepRange],
                    lux[index: index+sleepRange])
            
            lights_out_times.append(time[lights_out_index])
            lights_out_dates.append(date[lights_out_index])
            
            
        index = index + one_hour_epoch         # Check in increments of one hour
 
    
def get_in_bed_time_small_activity(date, time, activity, lux, study_period):
     """ Finds the lights out and got up times of a participant where 
    the days for which acitivity was recorded is less than the number
    of days the study was done over
    
    :param (array) time: the times at which the activity and light were recorded
    :param (array) activity: the activity for the specified epoch
    :param (array) lux: the lux for the specified epoch
    :return: Two lists containing the got up and lights out times of the 
        participant
    :rtype: (list) (list)  
    """    



def find_start_point(activity, study_period, start_threshold):
    """ Finds the point at which to start determining sleep points given an 
    activity array that is larger than the length of the study. 
    
    :param (array) activity: the activity counts for the participant
    :param (int) start_threshold: the threshold value for the number 
        of zeros allowed within an hour recording. Value used to determine
        when the actual recording for the motionwatch started given data 
        that exceeds the length of the study
    :param (int) study_period: the number of days they wore the motionwatch
    :return: returns the index at which to start the calculation
    :rtype: (int)
    """
    # The number of epochs in total neccesary for the requiried study length
    required_epoch_range = study_period*24*60
    # one hour is 60 epochs for one minute epoch length
    hour = 60
    start_index = 0
    for epoch_num in range(0, len(activity)):
        # check to see if we are exceeding the range of activity
        if (required_epoch_range + epoch_num >= len(activity)):
            break

        hour_range = activity[epoch_num:epoch_num+hour]
        num_zeros = count_zeros_in_array(hour_range)
        
        if(num_zeros < start_threshold):
           start_index = epoch_num 
        
    return start_index # if no clear cut start was found it's just going to use the begining of the activity
                        # data as the start point
      
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

def find_lights_out_index(activity, lux):
    """ Finds the lights out time of the participant given the start_index and
    sleep range
    :param (array) activity: the activity data of the participant over a sleep range
    :param (array) lux: the lux data of the participant over the sleep range
    :return: the index corresponding to the moment the participant went to sleep
    """
    

      