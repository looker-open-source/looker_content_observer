import click 
from _lco.dashboard import Dashboard
from _lco.dashboardchecker import DashboardChecker
from _lco.colorprint import ColorPrint
from _lco.test import TestResult
from setups.instance_config import config_instances
import logging
import pandas as pd


# TODO: Setup a ME() command to authenticate the API credentials

# https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

@click.group(name='run', help="Run the Multi Instance Dashboard Checker")
@click.pass_context
def run_lco(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Intializing Run")

# TODO: Turn run_all_lco with options to either read in a list from a file or take in a list from command line
@run_lco.command("all",help="Run a full test, test all dashboards")
@click.option('-f',
              '--file-path',
              'looker_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='File path for looker.ini (or equivalent) file.',
              default = 'looker.ini')
@click.pass_context
def run_all_lco(ctx,looker_file):
    logging.info("Testing all dashboards")
    pd.set_option('display.max_colwidth', None)
    dashboard_list = ["2","jhu_covid::jhu_base_template_extend","jhu_covid::sample_dashboard"]
    instances = config_instances()

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
            