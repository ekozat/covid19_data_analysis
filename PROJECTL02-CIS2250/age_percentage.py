'''
age_percentage.py
  Author(s): Jennifer Lithgow (1134108)
  //Earlier contributors(s): Sara Adi (1129361), Sophie Mlodzik (1130462), Andrew Hamilton-Wright, Kassy Raymond

  Project: COVID Analysis Project
  Date of Last Update: April 1, 2021.

  Functional Summary
      age_percentage.py takes in a CSV (comma separated version) file
      and outputs a new CSV file that can be graphed.

      There are expected to be three fields used:
          1. Date of infection
          2. Age range of infected
          3. Total population of age range
      
      There will be 2 fields in the output, in the form of a graph:
          1. Date of infection
          2. Percent of age range infected on a given day, 
              as a culmulative percentage over time

     Commandline Parameters: 5
        argv[0] = the python program to run
        argv[1] = name of the csv file containing census information
        argv[2] = name of the csv file containing infection information
        argv[3] = start of age range to calculate (inclusive)
        argv[4] = end of age range to calculate (exclusive)

     References
        Canadian Census of the Ontarian population:
          https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/dt-td/Rp-eng.cfm?TABID=1&LANG=E&A=R&APATH=3&DETAIL=0&DIM=0&FL=A&FREE=0&GC=35&GL=-1&GID=1161871&GK=1&GRP=1&O=D&PID=109526&PRID=0&PTYPE=109445&S=0&SHOWALL=0&SUB=0&Temporal=2016&THEME=115&VID=0&VNAMEE=&VNAMEF=&D1=0&D2=0&D3=0&D4=0&D5=0&D6=0
        Ontario Covid-19 Infection Data:
          https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350
'''

import sys
import csv

# seaborn and matplotlib are for plotting.  The matplotlib
# library is the actual graphics library, and seaborn provides
# a nice interface to produce plots more easily.
import seaborn as sns
from matplotlib import pyplot as plt

import numpy as np


#command line: filename to read census data from, filename to read infection data from, start of age range, end of age range (exclusive)
def main (argv):
  #make sure there's enough information
  if (len(argv) != 6):
    print("Usage: python age_percentage.py  <census filename> <covid-19 infections filename> <start decade> <end decade> <save file>")
    sys.exit(1)
  
  census_filename = argv[1]
  infection_filename = argv[2]
  age_start = int(argv[3])
  age_end = int(argv[4])
  save_file = argv[5]
  valid_information = True

  #check that the age range is valid
  if (age_start < 0 or age_end < 0):
    print("Age must be a positive number.")
    valid_information = False
  elif (age_end < 20):
    print("Minimum age for end of age range: 20 (restricted source data)")
    valid_information = False
  elif (age_end <= age_start):
    print("Invalid range. End of age range must be greater than the start.")
    valid_information = False
  elif( (age_start % 10) != 0 or (age_end % 10) != 0 ):
    print("Age ranges will be evaluated by approximate decade (rounded down). \nDo you wish to continue? \n(Enter n or N to end, any other input to continue)")
    user_input = input()
    if (user_input[0] == "n" or user_input[0] == "N"):
      valid_information = False
  else:
    valid_information = True

  if (age_end > 90) :
    print ("Due to restricted source data, all information for over \n90 years of age is conglomerated. \nDo you wish to continue? \n(Enter n or N to end, any other input to continue) ")
    uer_input = input()
    if (user_input[0] == "n" or user_input[0] == "N"):
      valid_information = False
  
  if (valid_information == False):
    print(valid_information)
    sys.exit(1)

  #adjust age start to make it "rounded down"
  age_start_adjusted = age_start - (age_start % 10)

  #open census file
  try:
    csv_census_path = open (census_filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}': {}".format(census_filename, err), file=sys.stderr)
    sys.exit(1)

  #csv read
  census_reader = csv.reader(csv_census_path)

  #gather needed census information in array; easier to handle while infection file is open
  #need to save
  sum_population = 0
  decade = 0
  for row in census_filename:
    for row_data_fields in census_reader:
      #print(row_data_fields)
      if (row_data_fields[0] == "Age_Group"):
        #ignore this row cuz it's just titles
        pass
      else :
        #print("Adjusted: {}".format(age_start_adjusted))
        if ( (decade >= age_start) and (decade < age_end) ):
          sum_population = sum_population + int(row_data_fields[1])
          #print("Decade: {}\tPopulation: {}".format(decade, sum_population))
        decade = decade + 10
        #print("{}\t{}".format(decade, row_data_fields[0]))

  csv_census_path.close()
  
  #open infection file
  try:
    csv_infection_path = open (infection_filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}': {}".format(infection_filename, err), file=sys.stderr)
    sys.exit(1)
  
  #csv read
  infect_reader = csv.reader(csv_infection_path)

  #gather population ages for every day
  #array 1: date, field 1
  #array 2: age range, field 2

  #date = []
  age_group_infected = 0
  #count = 0
  current_date = None
  #infected_population = 0
  percent = 0

  #lists for graphing/plotting
  date_infected = [] #x axis
  percent_infected = [] #y axis

  for row in infection_filename:
    for row_data_fields in infect_reader:
      #adding to the current date's sum
      if (current_date == None):
        current_date = row_data_fields[0]
      elif (current_date != row_data_fields[0]):
        #print title
        if (current_date == "Accurate_Episode_Date"):
          pass
          #print("Accurate_Episode_Date,Age_Group_Infected")
        else:
          percent = (age_group_infected / sum_population) * 100
          #restrict to 2 decimal points
          #print("{}\t{}\t{:.2f}".format(age_group_infected, sum_population, percent))
          #append to a list
          '''
          append date to list one: date_infected
          append percent infected to list two: percent_infected
          '''
          date_infected.append(current_date)
          percent_infected.append(percent)
        current_date = row_data_fields[0]
        #count = count + 1

      #find if it's in age range and add to total
      if (row_data_fields[2] == "<20"):
        if (age_start < 20) and (age_end >= 20) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "20s"):
        if (age_start < 30) and (age_end >= 30) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "30s"):
        if (age_start < 40) and (age_end >= 40) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "40s"):
        if (age_start < 50) and (age_end >= 50) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "50s"):
        if (age_start < 60) and (age_end >= 60) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "60s"):
        if (age_start < 70) and (age_end >= 70) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "70s"):
        if (age_start < 80) and (age_end >= 80) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "80s"):
        if (age_start < 90) and (age_end >= 90) :
          age_group_infected = age_group_infected + 1
      elif (row_data_fields[2] == "90+"):
        if (age_end > 90) :
          age_group_infected = age_group_infected + 1
  
  #Plotting
  '''
  #lists for graphing/plotting
  date_infected = [] #x axis
  percent_infected = [] #y axis
  '''
  info = [date_infected, percent_infected]

  #figure so that a visual is possible
  fig = plt.figure()

  #lineplot made via seaborn
  refig = sns.lineplot(x = date_infected, y = percent_infected)

  #reorganise/make plot cleaner
  refig.set(xlabel="Date Infected", ylabel="Percent Infected", title = 'Percent of Age Group Infected Over Time')

  #make labels a period of 90 days
  labels = []
  for count in range (0, len(date_infected), 90):
    labels.append(date_infected[count])

  x = np.arange(len(labels))
  refig.set_xticks(labels)
  refig.set_xticklabels(labels)
  fig.tight_layout()

  #save, export, and show
  fig.savefig ("Plotting/{}".format(save_file))

main(sys.argv)
