# Module: error_analysis
# Purpose: To perform error calculations on the in In Bed Times of the participants
# Author: Daniel Backhouse and Alan Yan
import matplotlib.pyplot as plt
import numpy as np

def get_error_per_day(program_part, protocol_part):
    """ Gets the absoulate error in the lights out or got up times
        of the participant for each day in minutes
    
    :param (array) program_part: the program determined times of the participant
    :param (array) protocol_part: the protocol determined times of the participant
    :return: An array containing the relative errors. If the error is greater
    than 12 hours it ignores this and returns an empty list
    :rtype: (arr)
    """
    participant_error = []
    index = 0
    while index < len(program_part) and  index < len(protocol_part):
        error = program_part[index] - protocol_part[index]
        error_min = abs(error.total_seconds()/60)
        participant_error.append(error_min)
        if(error_min >= 720):   # ignore all differences greater than 12 hours as 
            return list()       # this indicates different poins where chosen
        index = index + 1        
    return participant_error

def get_error_per_participant(LOdatesDic, LOprotocolDic, participant_list):
    """ Gets the absoulate error in the lights out or got up times
    for each participant in the whole study
    
    :param (array) LOdates: the program determined times of the study
    :param (array) LOprotocol: the protocol determined times of the study
    :param (array) participant_list: a list containing the participant ID's
    :return: A dictionary where the keys are the participant ID's and the values
    are arrays containing the relative errors of each day for each participant
    :rtype: (dic)
    """
    LOdates = list(LOdatesDic.values())
    LOprotocol = list(LOprotocolDic.values())
    error_per_participant = {}
    for i in range(0, len(LOdates)):
        print(participant_list[i])
        program_part = LOdates[i]
        protocol_part = LOprotocol[i]
        participant_error = get_error_per_day(program_part, protocol_part)
        error_per_participant[participant_list[i]] = participant_error
        
    return error_per_participant
    
def get_error_study(LOdatesDic, LOprotocolDic, participant_list):
    """ Gets the absoulate error in the lights out or got up times
    for each participant where the error values is the average error
    of each day in minutes
    
    :param (array) LOdates: the program determined times of the study
    :param (array) LOprotocol: the protocol determined times of the study
    :param (array) participant_list: a list containing the participant ID's
    :return: A dictionary where the keys are the participant ID's and the values
    are arrays containing the relative errors of each day for each participant
    summed over the entire study
    :rtype: (dic)
    """
    LOdates = list(LOdatesDic.values())
    LOprotocol = list(LOprotocolDic.values())
    error_dic = {}
    rel_participants = []
    for i in range(0, len(LOdates)):
        program_part = LOdates[i]
        protocol_part = LOprotocol[i]
        participant_error = __sum_errors(program_part, protocol_part)
        if(participant_error != 0):
            error_dic[participant_list[i]] = participant_error[0]
            rel_participants.append(participant_list[i])
        
    return error_dic, rel_participants

def __sum_errors(program_part, protocol_part):
    """ Sums the errors between two arrays
    
    :param (array) program_part: the program determined times of the participant
    :param (array) protocol_part: the protocol determined times of the participant
    :return: The absoualte value of the sum of the errors in minutes
    :rtype: (int)
    """
    participant_error = 0
    index = 0
    while index < len(program_part) and  index < len(protocol_part):
        error = program_part[index] - protocol_part[index]
        error_min = abs(error.total_seconds()/60)
        if(error_min >= 720):   # ignore all differences greater than 12 hours as 
            return 0     # this indicates different poins where chosen
        participant_error = error_min + participant_error
        index = index + 1
    if(index != 0 ):
        participant_error = participant_error/index
    return participant_error, 

def get_std_per_participant(LOdatesDic, LOprotocolDic, participant_list ):
    """ Gets the standard deviation in the error between the program and prtocol
    determined lights out or got up times
    
    :param (array) LOdates: the program determined times of the study
    :param (array) LOprotocol: the protocol determined times of the study
    :param (array) participant_list: a list containing the participant ID's
    :return: A dictionary where the keys are the participant ID's and the values
    are arrays containing the std deviation of the errors for each participant
    :rtype: (dic)
    """
    LOdates = list(LOdatesDic.values())
    LOprotocol = list(LOprotocolDic.values())
    std_per_participant = {}
    for i in range(0, len(LOdates)):
        program_part = LOdates[i]
        protocol_part = LOprotocol[i]
        participant_error = get_error_per_day(program_part, protocol_part)
        participant_std = np.std(participant_error, ddof = 1)
        std_per_participant[participant_list[i]] = participant_std  
    return std_per_participant
    
def plot_study_error(error_dic, participant_list):
    """ Plots the error of the study for each participant
    
    :param (array) error_arr: takes the error array of a participant
    :param (string) participant_id: the participant ID as a string
    :return: None
    """
    errors = list(error_dic.values())
    plt.plot(participant_list, errors,  'ro')   
    plt.ylabel('Absolute Error per Day')
    plt.xlabel('Participant ID')
    plt.title('Average Absolute Error Per Participant')
    #plt.rc('xtick', labelsize = 4)
    plt.xticks(fontsize=8, rotation=90)
    plt.ylim([0, 150])

def plot_participant_error(error_arr, participant_id):
    """ Plots the error of a single participant given an array and the participant ID 
    
    :param (array) error_arr: takes the error array of a participant
    :param (string) participant_id: the participant ID as a string
    :return: None
    """
    plt.plot(error_arr, 'ro')   
    plt.ylabel('Absolute Error in Minutes')
    plt.xlabel('Day # in Study')
    plt.title(participant_id)
    
def total_error(error_study):
    """ Sums all the average errors for each participant and returns one overall
    error value per participant
    
    :param (dic) error_study: an dictioantry where the values are floats
    :return: The error per participant in a study
    :rtype: float
    """
    error = list(error_study.values())
    average_error  = sum(error)/len(error)
    return average_error

def entries_over_fifteen(error_per_participant):
    """ Count the number of entries in each participant where the error
    is over 15
    
    :param 
    """
    count_per_participant = []
    for participant in list(error_per_participant.values()):
        fifteen_count = 0
        for error in participant:
            if error >= 30:
                fifteen_count = fifteen_count + 1
        count_per_participant.append(fifteen_count)    
        
    return sum(count_per_participant)

    