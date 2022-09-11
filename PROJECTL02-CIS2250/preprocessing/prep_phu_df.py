'''
prep_phu_df.py
  Author(s): Emily Kozatchiner (1149665)

  Project: COVID Analysis Project
  Date of Last Update: Mar 31, 2021.

  Functional Summary
      prep_phu_df.py preprocesses the given csv file into a more effecient data set to work with in the logic Script 

      There are expected to be three fields:
          1. phu_id
          2. phu_status (enumerated from file)
          3. start_date

      This code will produce a modified csv file from the original that gets created in the data folder and can be used for effeciency.

      The data file contains information on specific regions of PHUs across Ontario that are labelled a status. The time period of all of the effective statuses per PHU are recorded and stored.  

      Required information:
        Column 3 = PHU Id records
        Column 4 = PHU Status records
        Column 5 = Start date records

     Commandline Parameters: 2
        argv[1] = name of the csv file containing 

     References
        Name files from http://www.ssa.gov/OACT/babynames/limits.html
'''
#import all libraries
import pandas as pd
import sys

# Creation of dictionary to give all columns names for easier parsing of the data file (know what each column stores as data)
INDEX_MAP = {
        "_id" :  0,
        "Reporting_PHU" :  1,
        "Reporting_PHU_id" :  2,
        "Status_PHU" :  3,
        "start_date" :  4,
        "end_date" :  5,
        "PHU_url" :  6,
        }

def main(argv):
    # Checking for a correct nunmber input of parameters in order to errror catch if the code has been run incorrectly 
    if len(argv) != 2:
        print("Usage:",
                "preprocessing/prep_phu_df.py data/<data file>")
        sys.exit(-1)

    #take in the csv filename through parameter
    csv_filename = argv[1]

    # Open CSV file through pandas library - error catches if file is not readable for any reason
    try:
        csv_df = pd.read_csv(csv_filename)

    except IOError as err:
        print("Unable to open source file", csv_filename,
                ": {}".format(err), file=sys.stderr)
        sys.exit(-1)

    #enumerate data field of Status_PHU
    #NOTE: lockdown AND stay-at-home will have same scaling
    csv_df.loc[csv_df['Status_PHU'] == 'Prevent', 'Status_PHU'] = '1'
    csv_df.loc[csv_df['Status_PHU'] == 'Protect', 'Status_PHU'] = '2'
    csv_df.loc[csv_df['Status_PHU'] == 'Restrict', 'Status_PHU'] = '3'
    csv_df.loc[csv_df['Status_PHU'] == 'Control', 'Status_PHU'] = '4'
    csv_df.loc[(csv_df['Status_PHU'] == 'Lockdown') | (csv_df['Status_PHU'] == 'Stay-at-home'), 'Status_PHU'] = '5'
    csv_df.loc[csv_df['Status_PHU'] == 'Shutdown', 'Status_PHU'] = '6'

    #filtering unnecessary string data from the starting date
    csv_df['start_date'] = csv_df['start_date'].str.replace('T00:00:00', '') 

    #drop all data from unused columns 
    csv_df.drop(['_id', 'Reporting_PHU', 'end_date', 'PHU_url'], axis=1, inplace=True)
    
    #creates and saves modified csv to work with
    csv_df.to_csv("data/prep_phu_response.csv", index=False, encoding='utf8')
    #
    #   End of Function
    #

main(sys.argv)
#
#
#   End of Script
#