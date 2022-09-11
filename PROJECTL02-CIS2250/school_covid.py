'''
school_covid.py
  Author(s): Sara Adi (1129361)

  Project: COVID Analysis Project
  Date of Last Update: Mar 21, 2021.

  Functional Summary
      school_covid.py takes in data from two preprocessed files and then displays the relation between cases of COVID-19 among schools in Ontario, in comparison to the total cases the province sees that same day of specimen collection.

      The question to answer from the outputs of this file is:
        What is the relation between the number of confirmed positive Covid-19 cases within Ontario schools, vs. the total number of cases for Ontario as a province over time as a function of year and month?

      There are expected to be two fields used:
        From preprocessed_ontario.csv
            1. <collected_date>
            2. <specimen collected date?
            3. <age group of case>
        From prepprocessed_school_covid.csv
            1. <collected_date>
            2. <new_total_school_related_cases>

      Commandline Parameters: 3
        argv[0] = python script
        argv[1] = filename with school related data
        argv[2] = filename with Ontario data
        argv [3] = specified year of search
        argv [4] = specified month of search

      To run:
        python school_covid.py  data/preprocessed_school_covid.csv  data/preprocessed_ontario2.csv  <specified year > <specified month>

     References:
      N/A     
'''
#import all libraries

import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

#beginning of main
def main(argv):

  #ensure correct number of command line arguments
  if len(argv) != 5:
    print("Usage:","school_covid.py.py <data file>") 
    sys.exit(-1)
  #store command line arguments in appropriate variables
  csv_school_filename = argv[1]
  csv_ontario_filename =argv [2]
  year_of_search = argv [3]
  month_of_search = argv [4]
  #sets up the specified date (from command line) into one variable
  given_date = year_of_search + "-" + month_of_search
  #opens up a csv reader for the school covid csv file
  try:
    csv_path_school = open (csv_school_filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}' : {}".format(csv_school_filename, err), file=sys.stderr)
    sys.exit(1)
  
  school_file_reader = csv.reader(csv_path_school)
  #opens up a csv reader for the ontario covid csv file
  try:
    csv_path_ontario= open (csv_ontario_filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}' : {}".format(csv_ontario_filename, err), file=sys.stderr)
    sys.exit(1)
  
  ontario_file_reader = csv.reader(csv_path_ontario)
  #variables to keep track of total positive cases for the specifed term from command line
  school_total_cases = 0
  ontario_total_cases = 0
  #create a dictionary
  d={}
  #traverses the csv school reader data
  for row in school_file_reader:
    for row_data_fields in school_file_reader:
      given_date_in_file1 = row_data_fields [0]
      given_cases1 = row_data_fields[1]
      #only looks at the year-month, not the date
      temp_date1 = given_date_in_file1 [0:7]
      #ensures the data accounted for is within range specifed earlier
      if (given_date == temp_date1):
        #adds data to dictionary
        d[given_date_in_file1]=given_cases1
        #adds the total cases on the current day of the specifed year and month to total
        school_total_cases = school_total_cases + int (given_cases1)

  #creates dictionary and set
  d1 = {}
  s = set()

  #traverses the csv ontario reader data
  for row in ontario_file_reader:
    for row_data_fields in ontario_file_reader:
      given_date_in_file2 = row_data_fields [0]
      temp_date2 = given_date_in_file2 [0:7]
      #only looks at the year-month, not the date

      #ensures the data accounted for is within range specifed earlier
      if (temp_date2 == given_date):
        #adds one to the total num of province cases as each row is one person in this dataset
        ontario_total_cases+=1
        #if the date is already in the set, add one to the value
        if (given_date_in_file2 in s):
          d1 [given_date_in_file2]+=1
          
        #if the date is not in the set, add it to the dictionary's key and set. Set dictionary value to 1
        else:
          s.add(given_date_in_file2)
          d1[given_date_in_file2]=1
      

  #testing data stored
  #print ("School Data")
  #print(d)
  #print(match)
  #print ("Province Data")
  #print(d1)
      
  #if there exists cases for the specified term (from command line) for both the province and schools
  if ( (ontario_total_cases>0) and (school_total_cases>0)):
    final_percent = 100 - (((ontario_total_cases - school_total_cases) / ontario_total_cases) *100)
    print ("***COVID 19 SCHOOL + ONTARIO DATA***")
    print ("During the period of {}: ".format(given_date))
    print ("Total number of province-wide school cases: {} ".format(school_total_cases))
    print ("Total number of Ontario-wide cases: {} ".format(ontario_total_cases))
    print ("Percent of province-wide cases due to schools: {:.2f} %".format (final_percent))
  #if there exists cases for the specified term (from command line) for ONLY the province and not schools (different start dates from the datafiles makes this occur)
  elif ( (ontario_total_cases > 0) and (school_total_cases<1)):
    print ("***COVID 19 SCHOOL + ONTARIO DATA***")
    print ("During the period of {}: ".format(given_date))
    print ("There were NO reported school-wide cases at this time.")
    print ("Total number of Ontario-wide cases: {} ".format(ontario_total_cases))
    print ("Percent of province-wide cases due to schools: N/A")
  #if there does NOT exist cases for the specified term (from command line) for either schools or the province
  else:
    print ("***COVID 19 SCHOOL + ONTARIO DATA***")
    print ("During the period of {}: ".format(given_date))
    print ("There were NO reported school-wide cases at this time.")
    print ("There were NO reported province-wide cases at this time.")
    print ("Percent of province-wide cases due to schools: N/A")

  #plotting

  labels = ['Week 1','Week 2','Week 3','Week 4','Week 5']
  y=[] #for ontario data/week 
  z=[] #for school data/week
  i=1

  ontario_total_per_week=0
  school_total_per_week=0
  #loops through ontario dictionary created earlier, and gets total for each week of the month
  while i <= 7:
    data_of_key=given_date+"-0{}".format(i)
    if data_of_key in d1:
      ontario_total_per_week += d1[given_date+"-0{}".format(i)]
    i+=1
  y.append(ontario_total_per_week)
  ontario_total_per_week=0

  while (i<=14):
    if (i<=9):
      data_of_key=given_date+"-0{}".format(i)
      if data_of_key in d1:
        ontario_total_per_week += d1[given_date+"-0{}".format(i)]
      i+=1
    else:
      data_of_key=given_date+"-{}".format(i)
      if data_of_key in d1:
        ontario_total_per_week += d1[given_date+"-{}".format(i)]
      i+=1

  y.append(ontario_total_per_week)
  ontario_total_per_week=0  

  while i <= 21:
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d1:
      ontario_total_per_week += d1[given_date+"-{}".format(i)]
    i+=1
  y.append(ontario_total_per_week)
  ontario_total_per_week=0

  while i <= 28:
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d1:
      ontario_total_per_week += d1[given_date+"-{}".format(i)]
    i+=1
  y.append(ontario_total_per_week)
  ontario_total_per_week=0

  while i <= len(d1):
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d1:
      ontario_total_per_week += d1[given_date+"-{}".format(i)]
    i+=1
  y.append(ontario_total_per_week)
  ontario_total_per_week=0

  i=1
  #loops through school dictionary created earlier, and gets total for each week of the month
  while i <= 7:
    data_of_key=given_date+"-0{}".format(i)
    if data_of_key in d:
      school_total_per_week += int(d[given_date+"-0{}".format(i)])
    i+=1
  z.append(school_total_per_week)
  school_total_per_week=0

  while (i<=14):
    data_of_key=given_date+"-0{}".format(i)
    if (i<=9):
      if data_of_key in d:
        school_total_per_week += int(d[given_date+"-0{}".format(i)])
      i+=1
    else:
      data_of_key=given_date+"-{}".format(i)
      if data_of_key in d:
        school_total_per_week += int(d[given_date+"-{}".format(i)])
      i+=1

  z.append(school_total_per_week)
  school_total_per_week=0  

  while i <= 21:
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d:
      school_total_per_week += int(d[given_date+"-{}".format(i)])
    i+=1
  z.append(school_total_per_week)
  school_total_per_week=0

  while i <= 28:
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d:
      school_total_per_week += int(d[given_date+"-{}".format(i)])
    i+=1
  z.append(school_total_per_week)
  school_total_per_week=0

  while i <= 31:
    data_of_key=given_date+"-{}".format(i)
    if data_of_key in d:
      school_total_per_week += int(d[given_date+"-{}".format(i)])
    i+=1
  z.append(school_total_per_week)
  school_total_per_week=0
  
  #begins plotting data
  x=np.arange(len(labels))
  width=0.40
  fig,ax=plt.subplots()
  ax.bar(x - width/2, y, width, label='Ontario-wide')
  ax.bar(x + width/2, z, width, label='School-wide')

  # Add some text for labels, title and axis
  ax.set_ylabel('Number of Cases')
  ax.set_title('Number of Cases in Ontario vs. Schools Weekly')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()
  fig.tight_layout()
  #save, export, and show
  fig.savefig ("Plotting/school_plot.pdf")

main(sys.argv)
#end of main