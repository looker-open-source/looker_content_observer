from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
from dashboardchecker import DashboardChecker
from test import TestResult
import logging,configparser,argparse,yaml
from colorprint import ColorPrint
import pandas as pd

# dashboard_list = ["jhu_covid::jhu_base_template_extend","jhu_covid::sample_dashboard"]
# dashboard_list = [""]
dashboard_list = ["13"]#"data_block_acs_bigquery::testing_dashboard"] #13,"data_block_acs_bigquery::acs_census_overview"]
# look_list = ["13","14"]

def setup() -> dict:
    """
    Parses command line arguments and sets up logging.
    :returns: dictionary of argparse configurations
    """
    # Set argparse configuration, multiple instances get space delimited, see README
    parser = argparse.ArgumentParser(description='Arg to specify the instance to connect to.')
    parser.add_argument('--instance', '-i', type=str, nargs='+', help='Name of instance, as defined by the section within the looker.ini file')
    parser.add_argument('--environment','-e',type=str,nargs="+",choices=['production','dev'],default = 'production',help="Choose the environment to access, either production or dev")
    parser.add_argument('--loglevel', '-l', type=str, nargs="?", help='set the logging level',default =None, choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    parser.add_argument('--single', '-s', help='Run on a single instance+branch only',action='store_true')
    parser.add_argument('--csv', type=str,nargs="?", help='Store Data as a CSV',default=None)
    args = parser.parse_args()
    
    # Set logging configuration
    if args.loglevel:
        logging.basicConfig(level=getattr(logging,args.loglevel))
    
    logging.info(ColorPrint.yellow + f"main.setup:args passed in: {args}" + ColorPrint.end)
    return args.__dict__

def config_instances(argparse_dict:dict,looker_ini_file_path:str = "looker.ini") -> list:
    """
    - Reads API configuration for each instance, specific dev branch is specified in the looker.ini file (or looker.ini file equivalent)  
    :returns: list of instances to be tested
    """
    logging.info(ColorPrint.yellow + "Instantiating instances" + ColorPrint.end)
    # Append each instance as LookerEnvironment class to list
    instances = []

    for instance_index in range(len(argparse_dict.get('instance'))):
        config_instance_name, config_instance_environment = argparse_dict.get('instance')[instance_index], argparse_dict.get('environment')[instance_index]
        logging.info(ColorPrint.yellow + f"Starting connection to instance:{config_instance_name}, on {config_instance_environment}" + ColorPrint.end)
        try:
            instance_to_test = LookerEnvironment(config_instance_environment, config_instance=config_instance_name)
            # If we are testing a dev branch from an instance, we need to first checkout the dev branch in quest
            # Note: the code tested will based on the latest committed code, please commit any code changes prior to running script
            if config_instance_environment == 'dev':
                # The Looker project and dev branch are configured as keys within the looker.ini (or .ini equivalent file)
                config = configparser.ConfigParser()
                file = looker_ini_file_path
                config.read(file)
                logging.info(ColorPrint.yellow + f"Configuration file contains the following sections: {config._sections.keys()}" + ColorPrint.end)
                # Checkout dev branch of the instance, dev branch specified in the looker ini file
                instance_to_test.checkout_dev_branch(config._sections[config_instance_name]['project'],
                                                    config._sections[config_instance_name]['dev_branch'])
                logging.info(ColorPrint.green + "Succesfully checked out dev branch" + ColorPrint.end)
        except NameError: 
            print("Error in specifying the instance name, please confirm your argument matches an instance section from the looker.ini file")
        except:
            print("Error in setting the instance configurations")        
        # Append to instance list
        instances.append(instance_to_test)
    return instances

def config_tests_yaml(path_to_yaml_config_file:str="config_tests.yaml"):
    """
    - Reads in the tests specified within the "config_tests.yaml" file (or equivalent)
    :returns: list of tests read in from the config_file_yaml
    """
    try:
        with open(path_to_yaml_config_file, 'r') as file:
            tests = yaml.safe_load(file)
    except:
        logging.error("Error reading YAML File")

    logging.info(ColorPrint.yellow + f"Test file configuration {tests}" + ColorPrint.end)
    return tests

def run_dashboard_tests(dashboards_to_check:list,instances:list,tests_to_run:dict) -> tuple:
    """
    - Retrieves data for each test 
    :returns: each dashboard as element within list, all dashboards combined into a single pandas dataframe 
    """
    dash_data = []
    assert tests_to_run.get('dashboard_tests') is not None, f"No key found for dashboard tests, please confirm the config_tests.yaml file is being passed in"

    for dashboard_id in dashboards_to_check:
        dc = DashboardChecker(dashboard_id,
                              instances,
                              tests_to_run['dashboard_tests'])
        data = dc.get_data_for_test()
        logging.info(ColorPrint.yellow + f"Retrieved data for dash:{dashboard_id} of shape:{data.shape}" + ColorPrint.end)
        logging.info(ColorPrint.yellow + f"Applying pandas tests to data" + ColorPrint.end)
        # Apply test of equality
        data['is_data_equal'] = TestResult.is_data_equal(data)
        dash_data.append(data)
    
    return dash_data, pd.concat([*dash_data], ignore_index=True)

    
if __name__ == '__main__':
    # Run setup, parses the command line arguments and stores them into a dictionary called kwargs
    print(ColorPrint.green + "Step 1: Parsing command line arguments:" + ColorPrint.end)
    args = setup()
    
    print(ColorPrint.green + "Configuring list of instances to test:" + ColorPrint.end)
    # Retrieve a list of configured instances
    instances = config_instances(args)

    print(ColorPrint.green + "Configuring list of tests to run:" + ColorPrint.end)
    # Retrieve a list of tests to run on the instances
    tests_to_run = config_tests_yaml()

    print(ColorPrint.green +"Running Tests" + ColorPrint.end)
    # Run tests
    per_dashboard_dataframes, combined_dataframe = run_dashboard_tests(dashboard_list,instances,tests_to_run)
    logging.info(ColorPrint.yellow + f"Combined DataFrame:\n{combined_dataframe}" + ColorPrint.end)

    # Logging Errors on rows where the data is not equal between columns
    for key,row in combined_dataframe[combined_dataframe['is_data_equal'] == False].iterrows():
        print(ColorPrint.red + "Error on following test:" + ColorPrint.end)
        print(row,"\n")

    for key,row in combined_dataframe[combined_dataframe['is_data_equal'] == True].iterrows():
        print(ColorPrint.green + "Passed on following test:" + ColorPrint.end)
        print(row,"\n")


    # If optional arg for csv, create a CSV file
    if args.get('csv'):
        combined_dataframe.to_csv(args.get('csv'))


  