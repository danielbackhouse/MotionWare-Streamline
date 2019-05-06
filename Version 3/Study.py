""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
class Study:
    
    def __init__(self, sleep_analysis_directory, raw_data_directory, 
                 sleep_diary_directory, lights_out_index_diary, 
                 got_up_index_diary, lights_out_index_analysis, 
                 got_up_index_analysis, skiprows_diary, skiprows_analysis,
                 skiprows_rawdata):
        
        self.sleep_analysis_directory = sleep_analysis_directory
        self.raw_data_directory = raw_data_directory
        self.sleep_diary_directory = sleep_diary_directory
        self.lights_out_index_diary = lights_out_index_diary
        self.got_up_index_diary = got_up_index_diary
        self.lights_out_index_analysis = lights_out_index_analysis
        self.got_up_index_analysis = got_up_index_analysis
        self.skiprows_diary = skiprows_diary
        self.skiprows_analysis = skiprows_analysis
        self.skiprows_rawdata = skiprows_rawdata
        
        
    