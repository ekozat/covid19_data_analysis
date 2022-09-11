'''
prep_ontario.py
  Author(s): Sara Adi (1129361)

  Project: COVID Analysis Project
  Date of Last Update: Mar 17, 2021.

  Functional Summary
      prep_ontario.py takes in a CSV (comma separated version) file
      and pre-processes its content, and outputs to a second .csv file. his file will be sorted by Accurate_Episode_Date.

      There are expected to be two fields used:
          1. <collected_date>
          2. <specimen collected date?
          3. <age group of case>
        

      Commandline Parameters: 3
        argv[0] = python script
        argv[1] = filename with Ontario data, COL 2,6

      To run:
        python preprocessing/prep_ontario.py  data/conposcovidloc.csv
     
     References:
        N/A
        
'''
#import all libraries
import pandas as pd

import re
import csv
import sys

def main(argv):
  #pre proccessing second file

    csv_filename2 = argv[1]
    #try to create a dataset from panadas by reading the csv file 
    #provided from argv[1]
    try:
        data2 = pd.read_csv(csv_filename2)
    #if can not read file
    except IOError as err:
        print("Unable to open source file", csv_filename2,": {}".format(err), file=sys.stderr)
        sys.exit(-1)
    
    #drop all the columns that are not needed in the csv file
    #axis=1 tells pandas it is the columns and not rows that need to be dropped
    #inplace=True updates/shows the changes
    data2.drop(['Row_ID','Case_Reported_Date','Test_Reported_Date','Client_Gender','Case_AcquisitionInfo','Outcome1','Outbreak_Related','Reporting_PHU_ID','Reporting_PHU','Reporting_PHU_Address','Reporting_PHU_City','Reporting_PHU_Postal_Code','Reporting_PHU_Website','Reporting_PHU_Latitude','Reporting_PHU_Longitude'], axis=1, inplace=True)
    #creates a new csv file with the new preprocessed infromation

    data2["Accurate_Episode_Date"] = pd.to_datetime(data2["Accurate_Episode_Date"])
    data2 = data2.sort_values(by="Accurate_Episode_Date")

    data2.to_csv("data/preprocessed_ontario.csv", index=False, encoding='utf8')
    
    #drop all the columns that are not needed in the csv file
    #axis=1 tells pandas it is the columns and not rows that need to be dropped
    #inplace=True updates/shows the changes
    data2.drop(['Accurate_Episode_Date','Age_Group'], axis=1, inplace=True)
    #creates a new csv file with the new preprocessed infromation

    data2["Specimen_Date"] = pd.to_datetime(data2["Specimen_Date"])
    #data2 = data2.sort_values(by="Specimen_Date")

    data2.to_csv("data/preprocessed_ontario2.csv", index=False, encoding='utf8')

main(sys.argv)