# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click 
from _lco.colorprint import ColorPrint
from setups.instance_config import config_instances,config_tests
from setups.dashboard_run import run_dashboard_tests
from setups.look_run import run_look_tests
import logging
from pandas import set_option as pd_set_option
from datetime import datetime


# TODO: Scheduled changes - change all to 'content' --d and --l for the different types
# https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

@click.group(name='run', help="Run the Multi Instance Dashboard Checker")
@click.pass_context
def run_lco(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Intializing Run")

# TODO: Turn run_all_lco with options to either read in a list from a file or take in a list from command line
@run_lco.command("dash",help="Test a dashboard across instances and/or environments, multiple can be tested by chaining multiple -d <dash_1> -d <dash_2> etc..")
@click.option('-d',
              '--dashboard',
              'dashboard',
              type=click.STRING,
              help='Name, id, or slug of dashboard',
              multiple=True,
              required=True
              )
@click.option('-f',
              '--looker-file-path',
              'looker_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='File path for looker.ini (or equivalent) file.',
              default = 'looker.ini')
@click.option('-t',
              '--test-file-path',
              'test_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='Test Configurations Yaml File.',
              default = 'configs/config_tests.yaml')
@click.option('-csv',
              '--csv',
              'csv',
              type = str,
              help='Name of CSV file, default file name will be lco_dashboard_run_all_<date_time_of_run>.csv',
              default = '',
              required = False)
@click.pass_context
def run_dash_lco(ctx,
                dashboard:list,
                looker_file:str,
                test_file:str,
                csv:str):
    logging.info("Testing all dashboards")
    dashboard_list = dashboard
    instances = config_instances(looker_file)
    tests = config_tests(test_file)

    print(ColorPrint.green +"Running Tests" + ColorPrint.end)
    # Run tests
    per_dashboard_dataframes, combined_dataframe = run_dashboard_tests(dashboard_list,instances,tests)
    pd_set_option('display.max_columns', None)
    logging.info(ColorPrint.yellow + f"Combined DataFrame:\n{combined_dataframe}" + ColorPrint.end)
    # Logging Errors on rows where the data is not equal between columns
    for key,row in combined_dataframe[combined_dataframe['is_data_equal'] == False].iterrows():
        print(ColorPrint.red + "Error on following test:" + ColorPrint.end)
        print(row,"\n")

    # Logging cases where there was an individual tile API error
    for key,row in combined_dataframe["get_api_success" == combined_dataframe['test']].iterrows():
        # Check if any of the values have the failure key of "failed -" for logging
        if any("failed -" in str(val) for val in list(row)):                
            print(ColorPrint.red + "Failed retrieving API:" + ColorPrint.end)
            print(row,"\n")

    if csv != '':
        format_csv_string = lambda csv_string: csv_string.split(".")[0] if '.csv' in csv_string else csv_string   
        csv_file_name = datetime.now().strftime(f'outputs/dash_{format_csv_string(csv)}_%Y-%m-%d_%H%M%S.csv')
        combined_dataframe.to_csv(csv_file_name, index = False)


@run_lco.command("look",help="Test a Look across instances and/or environments, multiple can be tested by chaining multiple -l <look_1> -l <look_2> etc..")
@click.option('-l',
              '--look',
              'look',
              type=click.STRING,
              help='Name, id, or slug of Look',
              multiple=True,
              required=True
              )
@click.option('-f',
              '--looker-file-path',
              'looker_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='File path for looker.ini (or equivalent) file.',
              default = 'looker.ini')
@click.option('-t',
              '--test-file-path',
              'test_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='Test Configurations Yaml File.',
              default = 'configs/config_tests.yaml')
@click.option('-csv',
              '--csv',
              'csv',
              type = str,
              help='Name of CSV file, default file name will be lco_dashboard_run_all_<date_time_of_run>.csv',
              default = '',
              required = False)
@click.pass_context
def run_looks_lco(ctx,
                look:list,
                looker_file:str,
                test_file:str,
                csv:str):
    logging.info("Testing all dashboards")
    look_list = look
    instances = config_instances(looker_file)
    tests = config_tests(test_file)

    print(ColorPrint.green +"Running Test(s) on Look(s)" + ColorPrint.end)
    # Run tests
    per_look_dataframes, combined_dataframe = run_look_tests(look_list,
                                                                  instances,
                                                                  tests)
    logging.info(ColorPrint.yellow + f"Combined DataFrame:\n{combined_dataframe}" + ColorPrint.end)

    # Logging Errors on rows where the data is not equal between columns
    for key,row in combined_dataframe[combined_dataframe['is_data_equal'] == False].iterrows():
        print(ColorPrint.red + "Error on following test:" + ColorPrint.end)
        print(row,"\n")

    # Logging cases where there was an individual tile API error
    for key,row in combined_dataframe["get_api_success" == combined_dataframe['test']].iterrows():
        # Check if any of the values have the failure key of "failed -" for logging
        if any("failed -" in str(val) for val in list(row)):                
            print(ColorPrint.red + "Failed retrieving API:" + ColorPrint.end)
            print(row,"\n")

    if csv != '':
        format_csv_string = lambda csv_string: csv_string.split(".")[0] if '.csv' in csv_string else csv_string   
        csv_file_name = datetime.now().strftime(f'outputs/dash_{format_csv_string(csv)}_%Y-%m-%d_%H%M%S.csv')
        combined_dataframe.to_csv(csv_file_name, index=False)

@run_lco.command("me",help="Help confirm if API credentials have been configured correctly per instances")
@click.option('-f',
              '--file-path',
              'looker_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='File path for looker.ini (or equivalent) file.',
              default = 'looker.ini')
@click.pass_context
def test_api_instances(ctx,looker_file):
    instances = config_instances(looker_file)
    print("Testing API Connections:")
    for instance in instances: 
        print(f"Testing {instance.config_instance} instance API Credentials")
        try:
            me = instance.sdk.me() 
            print( ColorPrint.green +  f"API Connection Success. {instance}" + ColorPrint.end)
            logging.debug(ColorPrint.blue + f"Payload for auth check/me was: {me}")
        except:
            print("Error: Unable to conenct to API")
            