'''
phu_status.py
  Author(s): Emily Kozatchiner (1149665)
  Earlier contributors(s): Jennifer Lithgow, Andrew Hamilton-Wright, Kassy Raymond

  Project: COVID Analysis Project
  Date of Last Update: Mar 31, 2021.

  Functional Summary
      phu_status.py takes in

      There are expected to be three fields:
        From prep_phu_response.csv:
            1. phu_id
            2. phu_status (enumerated from file)
            3. start_date

      This code will calculate the rate of PHU status change between the adjacent start dates of a specific PHU status, and display the results. 
      It will also calculate the average rate of change throughout entire time period. 

      This file will display a positive or negative change in PHU severity per day and an overall status of how the public health measures have changed over time.

      Commandline Parameters: 3
        argv[1] = name of the csv file containing 
        argv[2] = a user chosen phu id
        
      To run:
        python phu_status.py data/prep_phu_response.csv <PHU id>

      References
        Name files from http://www.ssa.gov/OACT/babynames/limits.html
'''
#-1 For each date difference because end date is a day before the new start date IMPORTANT I actually dont know if its right

# Import libraries to work with inputted data and data plotting/visualizations
import csv
import sys
import seaborn as sns
from matplotlib import pyplot as plt

# Datatime library to work with date difference
from datetime import date

# Defined dictionary to give names to the required columns for effeciency and eligibility 
INDEX_MAP = {
        'Reporting_PHU_id' :  0,
        'Status_PHU' :  1,
        'start_date' :  2,
        }

# Function that calculates the date difference between two inputted dates. 
# Input:
#   Paramaters 1-3: A greater date parsed into integer values
#   Paramaters 4-6: A date less than the first one parsed     #   into integer values
def day_difference(year1, month1, day1, year2, month2, day2):
  
  f_date = date(int(year1), int(month1), int(day1))
  l_date = date(int(year2), int(month2), int(day2))

  return l_date - f_date

# main
def main(argv):
    # Ensures the user has eneted a correct amount of arguments in cmd
    if len(argv) != 3:
        print("Usage:","phu_status.py data/prep_phu_response.csv <phu_id>") 
        sys.exit(-1)
    
    filename = argv[1]
    phu_id = argv[2]

    #File error checking
    try:
        phudata_fh = open(filename, encoding="utf-8-sig")
    except IOError as err:
        print("Unable to open names file '{}' : {}".format(
                filename, err), file=sys.stderr)
        sys.exit(1)

    phudata_reader = csv.reader(phudata_fh)

    dates_arr = [] #x variable
    status_arr = [] #y variable

    # Variable used as bool to check for errors
    valid_input = 0

    #Date separator storage
    year_arr = []
    month_arr = []
    day_arr = []

    #reads data from csv file
    for row_data_fields in phudata_reader:
      
      # If PHU status is other - then skips the entire data row
      #if row_data_fields[INDEX_MAP['Status_PHU']] == 'Other':
      #  continue
      
      # Enters only if the inputted PHU id matches with a PHU id in the file
      if (row_data_fields[INDEX_MAP['Reporting_PHU_id']] == phu_id):
        dates = row_data_fields[INDEX_MAP['start_date']]
        dates_arr.append(dates)

        phu_status = row_data_fields[INDEX_MAP['Status_PHU']]
        status_arr.append(int(phu_status))

        if valid_input == 0:
          valid_input = 1
    
    # If the PHU id was never found in any of the datafile
    # Error checking
    if valid_input == 0:
      print("\nThe entered value for PHU id does not exist for the current used dataset.") 
      exit()
        
    concat_date_arr = []
    #holding arrays of values to calculate rate of change for each node
    diff_days = []
    diff_status = []
    #splitting the dates_arr string and separating values into own arrays (might need to remove enumerate)
    for num_dates, dates in enumerate(dates_arr):
      concat_date_arr = dates.split('-')
      #appends date values into separate arrays
      year_arr.append(concat_date_arr[0])
      month_arr.append(concat_date_arr[1])
      day_arr.append(concat_date_arr[2])

      if num_dates > 0:
        #calculates difference between each date and appends to array
        diff_days.append(day_difference(year_arr[num_dates-1], month_arr[num_dates-1], day_arr[num_dates-1], year_arr[num_dates], month_arr[num_dates], day_arr[num_dates]))

        #calcs difference between status and appends to array
        diff_status.append(status_arr[num_dates] - status_arr[num_dates-1])

    #calculates average difference between days and status for the total rate of change
    avg_diff_days = day_difference(year_arr[0], month_arr[0], day_arr[0], year_arr[-1], month_arr[-1], day_arr[-1])
    avg_diff_status = status_arr[-1] - status_arr[0]

    roc = []

    #calc rate of change between each difference    
    for num, dif in enumerate(diff_days):
      #calculates rate of change for each pair of adjacent dates
      roc.append(diff_status[num]/dif.days)

    #display results
    print("")
    print("*RESULTS*")
    print("Chosen PHU id: {}".format(phu_id))
    print("")
      
    for num, dates in enumerate(dates_arr):
      #Display all rate of changes
      if num > 0:
        print("The average rate of change in status between {} and {} is: {:.2f} change in PHU severity per day".format(dates_arr[num-1], dates, roc[num-1]))

    #Display total average rate of change
    avg_roc = avg_diff_status/avg_diff_days.days
    print("The average rate of change in severity in the PHU overall: {:.2f}".format(avg_roc))

    print("")

    #Displays overall change in status from the beginning of status label in a PHU to the end
    if avg_roc < 0:
      print("Overall, the change in status is positive (less dangerous in this PHU).")
    elif avg_roc > 0:
      print("Overall, the change in status is negative (more dangerous in this PHU).")
    else:
      print("Overall, there was no change in status.")

    #Plotting
    #set incrementation based on number of statuses
    y_increment = [1, 2, 3, 4, 5, 6]


    fig = plt.figure()
    refig = sns.lineplot(x = dates_arr, y = status_arr)

    #Set according labels and title of the graph for neat display
    refig.set(xlabel="Dates", ylabel="PHU status", title = "Rate of change for PHU status over time in PHU id: {}".format(phu_id))

    #set the y axis to increment by the list of statuses
    refig.set_yticks(y_increment)

    fig.tight_layout()

    #plt.show()

    #save graph to a pdf file in Plotting folder
    fig = plt
    fig.savefig ("Plotting/phu_plot.pdf")
    #
    #   End of Function
    #

main(sys.argv)
#
#
#   End of Script
#