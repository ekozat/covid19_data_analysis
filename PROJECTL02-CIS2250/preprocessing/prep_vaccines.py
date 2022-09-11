'''
prep_vaccines.py
  Author(s): Sophie Mlodzik (1130462)

  Project: COVID Analysis Project
  Date of Last Update: Mar 18, 2021.

  Functional Summary
      prep_vaccines.py takes in a CSV (comma separated version) file
      and prints out the fields.

      This python script reduces the number of columns of data in a file so that excess data is no longer included and the file will be easier to run when making calculations.

     Commandline Parameters: 2
        argv[0] = name of python script
        argv[1] = name of csv file containing vaccine data

     References
        Vaccine data file from https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario/resource/8a89caa9-511c-4568-af89-7f2174b4378c

      Command Line To Run 
        python preprocessing/prep_vaccines.py data/vaccines_administered.csv
'''

#import all libraries
import pandas as pd

#regex library
import re
import csv
import sys
        
def main(argv):
    #ensures there are the correct number of arguments
    if len(argv) != 2:
        print("Usage:","prep_vaccines.py <data file>") 
        sys.exit(-1)

    #PREPROCESSING
    #gather filename from command line
    csv_filename = argv[1]

    #try to create a dataset from pandas by reading the csv file provided by argv[1]
    try:
      csv_df = pd.read_csv(csv_filename)

    #if the file cannot be read, exit the program
    except IOError as err:
      print("Unable to open source file", csv_filename,": {}".format(err), file=sys.stderr)
      sys.exit(-1)

    #filtering unnecessary string data from the starting date
    csv_df['report_date'] = csv_df['report_date'].str.replace('T00:00:00', '') 

    csv_df['previous_day_doses_administered'] = csv_df['previous_day_doses_administered'].str.replace(',', '') 

    #drop the columns that are not needed for future calculations
    csv_df.drop(['_id','total_doses_administered','total_doses_in_fully_vaccinated_individuals','total_individuals_fully_vaccinated'], axis=1, inplace=True)

    #export remainder of data to a new csv file
    csv_df.to_csv("data/preprocessed_vaccines_administered.csv", index=False, encoding='utf8')

main(sys.argv)