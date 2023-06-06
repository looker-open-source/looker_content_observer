import click 
from _lco.dashboard import Dashboard
from _lco.dashboardchecker import DashboardChecker
from _lco.test import TestResult
import logging,configparser,argparse,yaml
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
@click.pass_context
def run_all_lco(ctx):
    logging.info("Testing all dashboards")
    pd.set_option('display.max_colwidth', None)
    dashboard_list = ["2","jhu_covid::jhu_base_template_extend","jhu_covid::sample_dashboard"]

