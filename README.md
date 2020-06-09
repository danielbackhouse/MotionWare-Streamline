# MotionWare-Streamline

This software is intended to be used with the Motion Watch 8 and MotionWare software. This
readMe will assume that you are currently using the Motion Watch 8 and MotionWare software
and are aware of how the Motion Watch 8 records data and how to export said data unto your 
computer in MotionWare's .mtn proprietary file format.

The algorithms used to find the light's out and get up times uses only uniaxial data to 
determine these points (even though the Motion Watch 8 has a triaxial setting). The sleep 
analysis itself is done with the algorithms and formulas used by the MotionWare software
(the manual with all these formulas can be found in this repository as well as the algorithim
we created to determine light's out and get up times). 

In order to for this software to work properly, please follow the protocol below:

Protocol

1. Download neccesary MotionWare software and python distribution (we use Python 3) +extensions on your computer. 
We recommend downloading Anaconda as it does not install Python into your PATH (unless of course 
you would like Python in your path in which case Anaconda offers that option too) and makes installing
the neccesary extension libraries easier.

2. The only required extension is Pandas (a Python Extension commonly used in data science). Open the 
Anaconda Prompt (which should have been installed when dowloading Anaconda) and type in the following:
- pip install pandas

3. Once the neccesary software is installed we have to use the MotionWare software to get the raw data files
containing lux and activity counts. 

4. Open the MotionWare software and click on 'Browse for MotionFile.'

5. Go to where your .mtn files are located and open them using the MotionWare software. An actigraph should
now appear graphically displaying the activity and lux counts recorded by the watch while it was active.

6. To make it easier to visualize, increase the activity scale reading to 1000 and the lux scale reading to 78.

7. Select the "Select Days" tab at the top of the program. Using your own discresion, pick a starting point
that begins at 12pm (it can be any day provided the data looks normal i.e. it is easy to see the user was wearing
the watch at this point). Now drag your cursor across all desired days over which to perform the sleep analysis
or all data that looks reasonable (WHICHEVER COMES FIRST). What makes data "reasonable" will be discussed further 
below.

8. Once your release the button on the mouse, a window should pop up. Click on Copy Raw Data. 

9. Open an excel spreadsheey and paste the data in the cell A1. Somewhere in the sheet you should
see the columns labelled "Date", "Time", "Activity", "Lux" (in this order). Make note of what
row these names appear in the sheet.

9. You should have created a folder somewhere on your computer and in that folder have sub folders named
"Baseline", "Midpoint", "Final" or something like this. Save your excel file in the sub folder of your choice.

10. Repeat steps 4-9 for all participants. 

11. Once all participants raw data files have been placed into their respective sub-folders, clone this 
repository somewhere on your computer. (this step can really be done at any time).

12. Open to RUN_MAIN_PROGRAM.py file. Follow the command line prompts.

13. Once you've enetered all reqiured fields the program will start to run. This should take roughyly 4 minutes
for 300 participants. 

14. The sleep analysis file with sheets labelled by participant should now be in your main subjects folder. 
If this has not happened, check the command line for the error that occured.

Notes: It is also possible to read sleep analysis files formatted in the same way the program outputs 
the sleep analysis files. This function however is only used to optimize the threshold values used for
the lights out get up algorithm and should probably not be tampered with.



*********** IGNORE BELOW THIS POINT ***********************
Concerning Formatting of Sleep Diary and Raw Data Excel Files:

It is very important that the TWO SEPERATE excel
files containing the raw data and sleep diary be formatted correctly BEFORE
using the MotionWare Analysis program. They must be formatted as follows:
(note that changes are being made to allow for improperly formatted documents
only the program will give an error).

Formatting Sleep Diary:
(example contained within Version 1 folder of this repository)

- The first column should specify the information present in their respective rows.
- The columns should be ordered:
	- ID Code (Cell A1)
	- Date (Cell A2)
	- Time tried to go to sleep (Cell A3)
	- Time finished trying to sleep (Cell A5)

- All subseuqent columns should containg relevant information where the date's proceed in
  chronological order. 

Formatting Raw Data Excel File:
(example contained within Version 1 folder of this repository)

- 3 columns of data (date and time, activity count and then lux count)
- first row holds strings specifying which column corresponds to which
- all subsequent rows should only include relevant data
- dates must be in chronological order

Concerning the Sleep Point Determination Method:

	The findSleepTime function:

		All the main computation for the sleep points is done within the 
		findSleepTime function. This function tracks and checks 4 important
		variables:

		- zeroMovementCount - number of consecutive time points with no activity detected
		- zeroLightCount - number of consecutive time points with no light detected
		- zeroLightActiveCount - number of consecutive time points with no activity AND THEN no light detected
		- darkMotion - number of consecutive timme points with no light AND THEN activity count below the mean
		
		Currently analysis has shown that dark motion is the best inidicator for study participant sleep times,
		although its effectivness on test populations other than members of the lab remains to be seen. 
		
		The threshold values for each of the four variables is set within the program and can be checked there. 
		Currently the threshold values work for members of the lab. Once one of the four variables exceeeds its
		threshold count we mark that time as being the sleep time and store that value. Note that the counts 
		represent the number of CONSECUTIVE occurences of each type and NOT an overall count within the given
		time range.
	
			



