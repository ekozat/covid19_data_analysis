'''
prep_school.py
  Author(s): Sara Adi (1129361)

  Project: COVID Analysis Project
  Date of Last Update: Mar 17, 2021.

  Functional Summary
      school_covid.py takes in a CSV (comma separated version) file
      and pre-processes its content, and outputs to a second .csv file.

      There are expected to be two fields used:
          1. <collected_date>
          2. <new_total_school_related_cases>

      Commandline Parameters: 3
        argv[0] = python script
        argv[1] = filename with school related data, COL 1, 5

      To run:
        python preprocessing/prep_school.py  data/schoolcovidsummary.csv

     References
        N/A
'''

#import all libraries
import pandas as pd

import re
import csv
import sys

def main(argv):
    #ensures there are the correct number of arguments
    if len(argv) != 2:
        print("Usage:","prep_school.py <data file>") 
        sys.exit(-1)
    
    #pre proccessing first file
    csv_filename = argv[1]
    #try to create a dataset from panadas by reading the csv file 
    #provided from argv[1]
    try:
        data = pd.read_csv(csv_filename)
    #if can not read file
    except IOError as err:
        print("Unable to open source file", csv_filename,": {}".format(err), file=sys.stderr)
        sys.exit(-1)
    
    #drop all the columns that are not needed in the csv file
    #axis=1 tells pandas it is the columns and not rows that need to be dropped
    #inplace=True updates/shows the changes
    data.drop(['reported_date','current_schools_w_cases','current_schools_closed','current_total_number_schools','new_school_related_student_cases','new_school_related_staff_cases','new_school_related_unspecified_cases','recent_total_school_related_cases','recent_school_related_student_cases','recent_school_related_staff_cases','recent_school_related_unspecified_cases','past_total_school_related_cases','past_school_related_student_cases','past_school_related_staff_cases','past_school_related_unspecified_cases','cumulative_school_related_cases','cumulative_school_related_student_cases','cumulative_school_related_staff_cases','cumulative_school_related_unspecified_cases'], axis=1, inplace=True)
    #creates a new csv file with the new preprocessed infromation
    data.to_csv("data/preprocessed_school_covid.csv", index=False, encoding='utf8')

main(sys.argv)

#fourth column, complete the addition