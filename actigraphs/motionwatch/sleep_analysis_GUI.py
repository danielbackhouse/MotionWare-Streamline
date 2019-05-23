# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:07:53 2019

@author: dbackhou
"""
from tkinter import *
from tkinter import filedialog
import run_sleep_analysis as run

window = Tk()
window.title("MotionWare Data Analysis")
window.geometry("500x450")

#Open Raw Data Directory
def openRawDataFile():
    filename = filedialog.askdirectory(initialdir = "/", title = 'Select folder')
    raw_data_entry.delete(0, END)
    raw_data_entry.insert(0, filename)
raw_data_label = Label(window, text = 'Enter the Raw Data Folder Path:')
raw_data_entry = Entry(window, width = 50)
raw_data_entry.insert(0, r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline")
openFileButton = Button(window, text = 'Open Folder', command = openRawDataFile)
raw_data_label.grid(row = 0, column = 0, columnspan = 3)
raw_data_entry.grid(row = 1, column = 0, columnspan = 2)
openFileButton.grid(row = 1, column = 2)

#Open Sleep Diary File
def openSleepDiaryFile():
    filename = filedialog.askopenfilename(initialdir = "/", title = 'Select folder')
    sleep_diary_entry.delete(0, END)
    sleep_diary_entry.insert(0, filename)
sleep_diary_label = Label(window, text = 'Enter the Sleep Diary File Path:')
sleep_diary_entry = Entry(window, width = 50)
sleep_diary_entry.insert(0, r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx")
openNewFileButton = Button(window, text = 'Open File', command = openSleepDiaryFile)
sleep_diary_label.grid(row = 2, column = 0, columnspan = 3)
sleep_diary_entry.grid(row = 3, column = 0, columnspan = 2)
openNewFileButton.grid(row = 3, column = 2)

#Skipped Rows
skipped_rows = StringVar(window)
skipped_rows.set(20) # default value
numbers = []
for x in range(100):
    numbers.append(x)
skipped_rows_list = OptionMenu(window, skipped_rows, *numbers)
skipped_rows_list.grid(row=5, column = 0, columnspan = 3)
skipped_rows_label = Label(window, text = 'Enter the Number of Rows To Skip in the Raw Data:')
skipped_rows_label.grid(row = 4, column = 0, columnspan = 3)


#Name of Study
name_study_label = Label(window, text = 'Enter the name of the study:')
name_study_entry = Entry(window, width = 50, justify = 'center')
name_study_entry.insert(0, 'BT')
name_study_label.grid(row = 6, column = 0, columnspan = 3)
name_study_entry.grid(row = 7, column = 0, columnspan = 3)

#Assessment 
assess_label = Label(window, text = 'Enter the assessment of the study:')
assess_entry = Entry(window, width = 50, justify = 'center')
assess_entry.insert(0, 'Baseline')
assess_label.grid(row = 8, column = 0, columnspan = 3)
assess_entry.grid(row = 9, column = 0, columnspan = 3)

#Trim Type
trim = StringVar(window)
trim.set(2) # default value
trim_list = OptionMenu(window, trim, 0, 1, 2)
trim_list.grid(row=11, column = 0, columnspan = 3)
trim_label = Label(window, text = 'Enter trim type:')
trim_label.grid(row = 10, column = 0, columnspan = 3)


#Start Button
def startGoing():
    raw_data_path = raw_data_entry.get()
    skipped_rows_num = int(skipped_rows.get())
    study_name = name_study_entry.get()
    assess = assess_entry.get()
    trim_num = int(trim.get())
    sleep_diary_path = sleep_diary_entry.get()
    print(raw_data_path)
    print(skipped_rows_num)
    print(study_name)
    print(assess)
    print(trim_num)
    print(sleep_diary_path)
    window.destroy()
    run.run_program(raw_data_path, skipped_rows_num, study_name, assess, trim_num, sleep_diary_path)
goButton = Button(window, text = 'Start', command = startGoing, width = 20, bg = 'green')
goButton.grid(row = 12, column = 2)

#Quit Button
quitButton = Button(window, text = 'QUIT', command = window.destroy, width = 20, bg = 'red')
quitButton.grid(row = 12, column = 0)



for x in range(3):
    window.columnconfigure(x, minsize = 500/3)
for y in range(18):
    window.rowconfigure(y ,pad = 10)
window.rowconfigure(12, pad = 40)
window.mainloop()