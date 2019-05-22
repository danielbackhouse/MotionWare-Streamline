# Module: error_analysis
# Author: Daniel Backhouse and Alan Yan

def get_error_participant(program_part, protocol_part):
    participant_error = []
    index = 0
    while index < len(program_part) and  index < len(protocol_part):
        error = program_part[index] - protocol_part[index]
        error_min = error.total_seconds()/60
        participant_error.append(error_min)
        index = index + 1
        
    return participant_error


def get_error_study(LOdates, LOprotocol, participant_list):
    study_error = []
    error_dic = {}
    for i in range(0, len(LOdates)):
        program_part = LOdates[i]
        protocol_part = LOprotocol[i]
        participant_error = get_error_participant(program_part, protocol_part)
        study_error.append(participant_error)
        error_dic[participant_list[i]] = participant_error
        
    return error_dic