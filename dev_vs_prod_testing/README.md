# Overview
Script to compare the dev vs. production data for a specific dashboard. Script is a proof of concept of the ways to pull data from different Looker branches (in this case production vs. a development branch) and compare the data that gets generated.  

## Example of Report (in Production):
![Production Version](/dev_vs_prod_testing/production_branch_of_report.png)

## Example of Report (in development after a change was made):
![Development Version](/dev_vs_prod_testing/development_branch_of_report.png)

## Example of the Output of the Script:
![Output of Script](/dev_vs_prod_testing/script_output_example.png)

## Output of Script
We can see from the screenshots an update was made to the first tile which caused the data within to get updated to (a potentially) wrong data point. The script outputs 2 dataframes (one from production, the other from the development branch). From here checks can be written to compare and test the two dataframes for any number of unit / data tests.