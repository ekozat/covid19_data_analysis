'''
vaccines_administered.py
  Author(s): Sophie Mlodzik (1130462)
  Earlier contributors(s): Sara Adi (1129361), Jennifer Lithgow (1134108), Andrew Hamilton-Wright, Kassy Raymond

  Project: COVID Analysis Project
  Date of Last Update: Apr 1, 2021.

  Functional Summary
      vaccines_administered.py takes in a CSV (comma separated version) file and prints out the fields.

      vaccines_administered.py takes in data regarding the number of covid vaccines that have been administered since December 2020 and uses it to predict the number of vaccines that will be administered on any given day in the near future.

     Commandline Parameters: 4
        argv[0] = name of python script
        argv[1] = name of csv file containing vaccine data
        argv[2] = name of graphics file
        argv[3] = number of days into the future

     References
        Vaccine data file from https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario/resource/8a89caa9-511c-4568-af89-7f2174b4378c

    Command Line to Run
    python vaccines_administered.py data/preprocessed_vaccines_administered.csv Plotting/vaccines_administered_plotting.pdf [number of days]

    **********
    ***ESSENTIAL***
    Every time the program is run, a new line is added to the csv file in order to graph the data.

    To avoid this impacting future graphs and skewing the data, you must MANUALLY delete the last row in "data/preprocessed_vaccines_administered.csv", row 95, before running the program again.
    **********
'''

import pandas as pd

#regex library
import re
import csv
import sys

#seaborn and matplotlib are for plotting.  The matplotlib library is the actual graphics library, and seaborn provides a nice interface to produce plots more easily.
import seaborn as sns
from matplotlib import pyplot as plt
        
def main(argv):
  #ensures there are the correct number of arguments
  if len(argv) != 4:
    print("Usage:","vaccines_administered.py <data file> <graphics filename>") 
    sys.exit(-1)

  #create variables to store command line arguments
  filename = argv[1]
  graphics_name = argv[2]
  num_days = argv[3]

  #try to open the csv file, print error message if unable to do so
  try:
    open_file = open(filename, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open file name '{}' : {}".format(filename, err), file=sys.stderr)
    sys.exit(1)

  #create a variable for the csv reader
  file_reader = csv.reader(open_file)

  #now that all input checking is done, create any additional variables
  row_count = 0
  start_row = 0
  average_rate_of_growth = 0.0
  predicted_num_vaccines = 0.0
  temp = "temp"
  all_days = []
  last_30_days = []
  rate_of_growth = []

  #count the number of rows
  #remove the commas from the numbers to avoid math errors later on
  for row in file_reader:
    for row_data_fields in file_reader:
      row_count += 1
      temp = row_data_fields[1].replace(',', '')
      all_days.append(temp)

  #calculate what row to start on
  start_row = row_count - 30  

  #reset the row count to iterate through it again
  row_count = 0
  #add only the last 30 days to a new list for calculations
  for num in all_days:
    row_count += 1
    if (row_count >= start_row):
      last_30_days.append(num)
    
  #calculate the rate of growth between each day
  #add each to an array of decimal values
  for num in range(0, (len(last_30_days)-1)):
    rate_of_growth.append(int(last_30_days[num+1])/int(last_30_days[num]))

  #find the average rate of growth over the last 30 days
  for num in rate_of_growth:
    average_rate_of_growth += num

  average_rate_of_growth = average_rate_of_growth / 30

  #predict the number of vaccines administered num_days into the future
  predicted_num_vaccines = float(last_30_days[29])
  for num in range(0, int(num_days)):
    predicted_num_vaccines = predicted_num_vaccines * average_rate_of_growth

  #convert to an int for printing
  predicted_num_vaccines = int(predicted_num_vaccines)

  #use "*" between lines to make the output easier to read
  #print the average rate of growth
  #print the predicted number of vaccines
  if (int(num_days) <= 30):
    print("**********")
    print("The average rate of growth of the number of vaccines administered in the last 30 days is: ", average_rate_of_growth)
    print("**********")
    print("Prediction: in {} days, {} vaccines will be administered.".format(num_days, predicted_num_vaccines))
    print("**********")
  else:
    print("**********")
    print("Due to the fact that the rate at which vaccines are being administered at is constantly changing, a prediction cannot be made for more than 30 days into the future.")
    print("**********")

  #PLOTTING
  #add a new row to the end of the csv file so it can be plotted
  with open('data/preprocessed_vaccines_administered.csv', 'a') as fd:
    fd.write("\n2021-04-05,{}".format(predicted_num_vaccines))

  # Open the data file using "pandas", which will attempt to read in the entire CSV file
  try:
    csv_df = pd.read_csv(filename)
  except IOError as err:
    print("Unable to open file name '{}': {}".format(filename, err), file=sys.stderr)
    sys.exit(1)

  #figure so that a visual is possible
  fig = plt.figure()

  #lineplot made via seaborn
  sns.lineplot(x = "report_date", y = "previous_day_doses_administered", data=csv_df)

  #save to a file
  fig.savefig (graphics_name, bbox_inches="tight")
  #plt.show()

main(sys.argv)