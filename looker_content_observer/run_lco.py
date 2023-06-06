import click 
from _lco.colorprint import ColorPrint
from setups.instance_config import config_instances,config_tests
from setups.dashboard_run import run_dashboard_tests
import logging
from datetime import datetime

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
@click.option('-csv/-no-csv',
              '--csv/--no-csv',
              'csv',
              type = bool,
              help='Boolean to output create a csv file. Note specify a --csv-name after using this flag',
              default = False,
              required = False)
@click.option('-csv-name',
              '--csv-name',
              'csv_name',
              type = str,
              help='Name of CSV file, default file name will be lco_dashboard_run_all_<date_time_of_run>.csv',
              default = 'test.csv',
              required = False)
@click.pass_context
def run_all_lco(ctx,
                looker_file:str,
                test_file:str,
                csv:bool,
                csv_name:str):
    logging.info("Testing all dashboards")
    dashboard_list = ["2","jhu_covid::jhu_base_template_extend","jhu_covid::sample_dashboard"]
    instances = config_instances(looker_file)
    tests = config_tests(test_file)

    print(ColorPrint.green +"Running Tests" + ColorPrint.end)
    # Run tests
    per_dashboard_dataframes, combined_dataframe = run_dashboard_tests(dashboard_list,instances,tests)
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

    if csv: 
        csv_file_name = datetime.now().strftime(f'{csv_name}_%H_%M_%d_%m_%Y.csv')
        combined_dataframe.to_csv(csv_file_name)


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
            