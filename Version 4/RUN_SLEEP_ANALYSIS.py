""" Title: RUN_SLEEP_ANALYSIS
    Purpose: 
        *******************IMPORTANT PLEASE READ***************************
        This is the main program and SHOULD be used to run the sleep analysis
        (it shoulda also be the only file you need to open).
        DO NOT make any changes to any of the other files within the program.
        It is recomondded that you only change the variables specified. There
        should be an explanation of what each variable does
        
    Author: Alan Yan and Daniel Backhouse
"""
import Study
import SleepDataAnalysis
# Sleep Analysis Directory: enter the sleep analysis directory within the double
# quotations. NOTE THAT THIS FIELD IS NOT REQUIRED AND IS ONLY NEEDED IF COMPARING
# PROGGRAM VALUES TO PROTOCOL VALUES. So then if there is no sleep analysis directory
# just leave enter r"" after the equals sign.
sleep_analysis_directory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'

# Indicies and SkipRows Analysis: THESE ARE NOT REQUIRED IF NO SLEEP ANALYSIS DIRECTORY
# IS SPECIFIED. These indices should not be changed unless the format of the 
# sleep analysis files is different
lights_out_index_analysis = 2
got_up_index_analysis = 5
skiprows_analysis = 16


# Sleep Diary Directory: THIS IS A REQUIRED FIELD. Enter the directory where the 
# sleep diary excel files is located.
sleep_diary_directory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\Edited Sleep Diary\BT Sleep Diary Edited.xlsx'

# Indices and SkipRows Sleep Diary: THESE FIELDS ARE REQUIRED. These should not
# be changed unless the file format for the sleep diaries is changed
lights_out_index_diary = 1;
got_up_index_diary = 5;
skiprows_diary = 0;


# Raw Data Directory: THIS IS A REQUIRED FIELD. Enter the directory where the 
# raw data files are located. The raw data files should be in folders Baseline
# Midpoint and Final
raw_data_directory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data'

# SkipRows Raw Data: THIS IS A REQUIRED FIELD. This field should not be changed 
# unless the format of the raw data files has changed. This field is the most
# likely to vary between study
skiprows_rawdata = 12

# study_name: THIS IS A REQUIRED FIELD. Enter within the qoutations the
# abbreviation of the study. An examplen entry would be: "BT" or "FACT".
study_name = "BT"

# assesment: THIS A REQUIRED FIELD. Enter whether you want to analyze Baseline,
# Midpoint or Final. Valid entries then are: "Baseline", "Midpoint", "Final."
assesment = "Baseline"

# *************DO NOT MAKE CHANGES TO THE PROGRAM BEYOND THIS POINT**********

sleep_study = Study.Study(sleep_analysis_directory, raw_data_directory, 
                          sleep_diary_directory, lights_out_index_diary, 
                          got_up_index_diary, lights_out_index_analysis, 
                          got_up_index_analysis, skiprows_diary, 
                          skiprows_analysis, skiprows_rawdata, 
                          study_name, assesment)

LOdates, LOtimes ,GUdates , GUtimes = sleep_study.get_in_bed_times_noDiary()


sleep_study.use_sleep_diaries()


rawData = sleep_study.raw_data_withDiary
LO_program, GU_program = sleep_study.get_study_program_times()
LO_analysis, GU_analysis = sleep_study.get_study_analysis_sleep_times()


error = sleep_study.error_in_date_time_lists(LO_program,LO_analysis)

sleepAnalysis = list()
for i in range(0,len(GU_program)):
    print(i)
    for j in range(0,len(GU_program[i])):
        participant_awake = GU_program[i]
        participant_sleep = LO_program[i]
        dictionary = SleepDataAnalysis.findSleepAnalysisData(
                participant_sleep[j], participant_awake[j], rawData[i])
        sleepAnalysis.append(dictionary)




