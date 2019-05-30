""" Title: RUN_SLEEP_ANALYSIS
    Purpose: 
        *******************IMPORTANT PLEASE READ***************************
        This is the main program and SHOULD be used to run the sleep analysis
        (it should also be the only file you need to open).
        DO NOT make any changes to any of the other files within the program.
        It is recomondded that you only change the variables specified. There
        should be an explanation of what each variable does
        
    Author: Alan Yan and Daniel Backhouse
"""
import create.Study as study
import create.ProtocolSleepAnalysis as ps
import optimize.threshold_optimization as thresh
import compute.error_analysis as err

raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Baseline"
trim_type = 2
ws = 6
dm = 12 
zac = 25
zmc = 180
zlc = 180
ta = 20 




sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)

protocol = ps.ProtocolSleepAnalysis(sa_directory, sleep_study.participant_list,
                                    study_name, assesment)
LOprotocol, GUprotocol, LOdicProtocol = protocol.get_study_analysis_sleep_times()

#error_averages, std_study, count, indices, errors = thresh.optimize_LO_times(sleep_study, LOprotocol)

LO, GU, SI, PL, LOdicProgram = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)
error_study, RP = err.get_error_study(LO,LOprotocol,PL)
error_per_participant = err.get_error_per_participant(LO, LOprotocol, PL)
count = err.entries_over_fifteen(error_per_participant)
error = err.total_error(error_study)
