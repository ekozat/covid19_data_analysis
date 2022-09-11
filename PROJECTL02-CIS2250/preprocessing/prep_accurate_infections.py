'''
prep_accurate_infections.py

  UPDATE: Altered, incorporated into main function

  Author(s): Jennifer Lithgow (1134108)
  //Earlier contributors(s): 

  Project: COVID Analysis Project
  Date of Last Update: Mar 27, 2021.

  Functional Summary
      prep_accurate_infections.py takes in a CSV (comma separated version) file
      and outputs a new CSV file for further processing.

      There are expected to be two fields used:
          1. <accurate date of infection>
          2. <age range of infected>
      
      There will be 2 fields in the output:
          1. date of infection
          2. age range of infected

     Commandline Parameters: <how many>
        argv[0] = the python program to run
        argv[1] = name of the csv file containing infection data

     References
        Name files from <link to>
'''

import sys
import csv

def main (argv):
  #make sure there's enough information
  if (len(argv) != 2):
    print("Usage: python prep_accurate_infections.py  <filename>")
    sys.exit(1)
  
  filename = argv[1]

  #open file
  try:
    csv_path = open (filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}': {}".format(filename, err), file=sys.stderr)
    sys.exit(1)

  #csv read
  reader = csv.reader(csv_path)

  count = 0
  current_date = None
  infected_population = 0

  for row in filename:
    for row_data_fields in reader:
      if (current_date == None):
        current_date = row_data_fields[0]
      if (current_date == row_data_fields[0]):
        count = count + 1
        #find if it's in age range
      else :
        print("{},{}".format(current_date, count))
        current_date = row_data_fields[0]
        #

main (sys.argv)