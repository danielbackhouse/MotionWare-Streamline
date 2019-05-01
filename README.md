# MotionWare-Streamline

Concerning Formatting of Sleep Diary and Raw Data Excel Files:

It is of the utmost and paramount importance that the TWO SEPERATE excel
files containing the raw data and sleep diary be formatted correctly BEFORE
using the MotionWare Analysis program. They must be formatted as follows:

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
		represent the number of CONSECUTIVE occurences of each type and NOT an overall count with the given
		time range.
	
			
TODO



