# Cropsim Weather

## App Description
This program is designed to take raw, exported weather station files as .csv's from http://awdn.unl.edu/classic/stnsel.cgi
and go through each station (one station per csv file) and break this file into a format that can be used by CropSim.

CropSim needs yearly input. For the 1953-2020 period, this produces 67 individual files. 
This program will output those 67 files for each .csv file, looping through the files. 

### University of Nebraska Lincoln Website
http://awdn.unl.edu/classic/stnsel.cgi

* Username: thad
* Password: scottsBluff19

### File Location
The following section of code is specific to the user running the program and should be updated to reflect the correct 
file locations:

`file_path = "C:/Users/Jason/Desktop/weather_data_master/`

### Station Data
Station data is stored in the main.py file, under `station_data` as a dictionary. 
This inclues the weather station name as a key, with the following data as values:

* Position 0 : Latitude
* Position 1 : Longitude
* Position 2 : Elevation (feet)
* Position 3 : National Weather Service Code

