'''
prep_census.py
  Author(s): Jennifer Lithgow (1134108)
  //Earlier contributors(s): Sara Adi (1129361)

  Project: COVID Analysis Project
  Date of Last Update: Mar 18, 2021.

  Functional Summary
      prep_census.py takes in a CSV (comma separated version) file
      and outputs a new CSV file better suited to desired analysis.
      This means compiling populations into decade age ranges, as 
      that is the same available for "age of infection" for this 
      cross-file analysis.

  Constraints:
      Covid infection data has created a restriction on age ranges.
      Age populations will be documented as:
        <20, 20s, 30s,..., 80s, 90+
      age_percentage.py will alert the user to these restrictions at
      the time of excecution.

  There are expected to be two fields kept:
      1. Age_Group, denoted in the same format as preprocessed_ontario.csv
      2. Total population of age range by decade

  Commandline Parameters: 2
      argv[0] = the python program to run
      argv[1] = name of the csv file to reformat/recompile

  References
    Canadian Census of the Ontarian population:
      https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/dt-td/Rp-eng.cfm?TABID=1&LANG=E&A=R&APATH=3&DETAIL=0&DIM=0&FL=A&FREE=0&GC=35&GL=-1&GID=1161871&GK=1&GRP=1&O=D&PID=109526&PRID=0&PTYPE=109445&S=0&SHOWALL=0&SUB=0&Temporal=2016&THEME=115&VID=0&VNAMEE=&VNAMEF=&D1=0&D2=0&D3=0&D4=0&D5=0&D6=0
'''

#import libraries
import pandas as pd

import re
import csv
import sys

def main (argv):
  if len(argv) != 2:
      print("To use this program, write:")
      print("python preprocessing/prep_census.py <csv filename to read>")
      sys.exit(-1)

  #load data
  #filename = 'data/mini_census_check.csv'
  filename = argv[1]
  #'data/109 526 202 103 170 925 05.CSV'

  try:
      file_csv = pd.read_csv(filename)
      #if can not read file
  except IOError as err:
      print("Unable to open source file", filename,": {}".format(err), file=sys.stderr)
      sys.exit(-1)

  '''
  The following lines filter the data so that age and row index 'match'
  This means that, using the index, ages can be more easily filtered and added up
  '''
  #remove rows that are ranges (x to y years)
  file_csv = file_csv.loc[~(file_csv ["Age (in single years) and average age (127)"].str.contains('to'))]
  #remove 'total' row, unnecessary (timestamp 39:29)
  file_csv = file_csv.loc[~(file_csv ["Age (in single years) and average age (127)"].str.contains('Total - Age'))]
  #remove extra "telling" lines that are unnecessary
  file_csv = file_csv.loc[~(file_csv ["Age (in single years) and average age (127)"].str.contains('65 years and over'))]
  file_csv = file_csv.loc[~(file_csv ["Age (in single years) and average age (127)"].str.contains('85 years and over'))]
  #reset index of rows
  file_csv.reset_index(drop=True, inplace = True)
  #print(file_csv)

  #print new titles to csv
  print("Age_Group,Population")

  sum = 0
  for index, row in file_csv.iterrows():
    if (index % 10 == 0) and (index > 10):
      if (index <= 20):
        print("<20,{}".format(sum))
        sum = 0
      elif (index > 90):
        sum = sum
        #print("90+,{}".format(sum))
        #this is the final sum printed
        #it will be printed after exiting loop to avoid missing data
      else:
        print("{}s,{}".format(index - 10, sum))
        sum = 0
    
    
    if index < 20:
      sum = sum + file_csv.iloc[index,1]
      #print("{}--{}".format(index,file_csv.iloc[index,1]))
      #file_csv.loc["Total - Sex"]

    elif index < 30:
      #people in their 20s
      sum = sum + file_csv.iloc[index,1]
    elif index < 40:
      #people in their 30s
      sum = sum + file_csv.iloc[index,1]
    elif index < 50:
      #people in their 40s
      sum = sum + file_csv.iloc[index,1]
    elif index < 60:
      #people in their 50s
      sum = sum + file_csv.iloc[index,1]
    elif index < 70:
      #people in their 60s
      sum = sum + file_csv.iloc[index,1]
    elif index < 80:
      #people in their 70s
      sum = sum + file_csv.iloc[index,1]
    elif index < 90:
      #people in their 80s
      sum = sum + file_csv.iloc[index,1]
    else:
      #people in their 90s or older
      sum = sum + file_csv.iloc[index,1]
  
  print("90+,{}".format(sum))
    

  #for index, row in file_csv.iterrows():
    #print(index, row["Age (in single years) and average age (127)"], row["Total - Sex"])
    #works when it has spaces: print(file_csv.loc[file_csv['Age (in single years) and average age (127)'] == '      5'])

    #Change age to match the type available in infections csv file
    #if 'Age' = 'under 1 year'
      #add to sum of <20
      #age_num += 1
    #if ['Age (in single years) and average age (127)'] == '      {}'.format(age_num)
      #if age_num % 10 == 0 #age_num
        #print sum to new file
        #print("{},{}".format(index - 10, sum)) #subtract 10 so it's the previous decade's 'label'
        #reset sum to 0
      
      #if age_num < 20
        #add to sum of <20
      #elif 20-29
      #elif 30-39
      #...
      #elif 90+

      #age_num += 1
  
  #file_csv.to_csv("data/preprocessed_census.csv", index=False, encoding='utf8')
  #file_csv.to_csv("census_testing_output.csv", index=False, encoding='utf8')

main(sys.argv)

'''
def main(argv):
    #creates a new csv file with the new preprocessed infromation

    data2["Accurate_Episode_Date"] = pd.to_datetime(data2["Accurate_Episode_Date"])
    data2 = data2.sort_values(by="Accurate_Episode_Date")
'''