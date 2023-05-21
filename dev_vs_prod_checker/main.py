from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
from dashboardchecker import DashboardChecker
from dashboardcheckersingle import DashboardCheckerSingle
from lookcheckersingle import LookCheckerSingle
import logging
import configparser
import argparse
from colorprint import ColorPrint
import pandas as pd

dashboard_list = ["jhu_covid::jhu_base_template_extend","2"]
# dashboard_list = [""]
# dashboard_list = ["13","data_block_acs_bigquery::testing_dashboard"] #,"data_block_acs_bigquery::acs_census_overview"]
look_list = ["13","14"]

def setup() -> dict:
    """
    :returns: dictionary of argparse configurations
    """
    # Set argparse configuration, multiple instances get space delimited, see README
    parser = argparse.ArgumentParser(description='Arg to specify the instance to connect to.')
    parser.add_argument('--instance', '-i', type=str, nargs='+', help='Name of instance, as defined by the section within the looker.ini file')
    parser.add_argument('--environment','-e',type=str,nargs="+",choices=['production','dev'],default = 'production',help="Choose the environment to access, either production or dev")
    parser.add_argument('--loglevel', '-l', type=str, nargs="?", help='set the logging level',default =None, choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    parser.add_argument('--single', '-s', help='Run on a single instance+branch only',action='store_true')
    args = parser.parse_args()
    
    # Set logging configuration
    if args.loglevel:
        logging.basicConfig(level=getattr(logging,args.loglevel))
    
    logging.info(ColorPrint.yellow + f"main.setup:args passed in: {args}" + ColorPrint.end)
    return args.__dict__

def config_instances(argparse_dict:dict,looker_ini_file_path:str = "looker.ini") -> list:
    """
    :returns: list of instances to be tested
    """
    logging.info(ColorPrint.yellow + "Instantiating instances" + ColorPrint.end)
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

def config_tests(path_to_config_file:str= "config_tests.ini"):
    # Read config.ini file which contains the individual tests which can be run
    config = configparser.ConfigParser()
    file = path_to_config_file
    config.read(file)
    logging.info(ColorPrint.yellow + f"Test file configuration {config._sections}" + ColorPrint.end)

    # Collect dashboard level tests    
    dashboard_tests = []
    for test,run_test in config._sections['Dashboard'].items():
        if run_test.lower() == "true":
            dashboard_tests.append(test)

    # Collect look level tests
    look_tests = []
    for test,run_test in config._sections['Look'].items():
        if run_test.lower() == "true":
            look_tests.append(test)

    logging.info(ColorPrint.yellow + f"Dashboards will be tested for the following: {dashboard_tests}" + ColorPrint.end)
    logging.info(ColorPrint.yellow + f"Looks will be tested for the following: {look_tests}" + ColorPrint.end)
    return dashboard_tests, look_tests

def run_tests(dashboards_to_check:list,instances:list,dashboard_tests:list,look_tests:list=look_list):
    for dashboard_id in dashboards_to_check:
        dc = DashboardChecker(dashboard_id,
                              instances,
                              dashboard_tests)
        dc.get_data_for_test()
        logging.debug(ColorPrint.blue + f"Retrieve data for dash:{dashboard_id}: {dc.test_results}" + ColorPrint.end)





# def run_dashboard_tests(tests_to_run,**kwargs):
#     for dashboard_to_test in dashboard_list:   
#         if kwargs['single']:
#             dc = DashboardCheckerSingle(dashboard_to_test,kwargs,instances[0],tests_to_run)
#             dc.run_tests()
#             dc.output_tests()

#         else:
#             dc = DashboardChecker(dashboard_to_test,kwargs,*instances,tests_to_run)
                
#             # to do: create a dc.run_tests method
#             # Step 1: Run the tests
#             dc.run_tests()

#             # Step 2: Log and print out the outputs
#             dc.output_tests()

#             # Step 3: Output a dataframe we can turn into a CSV
#             # print("\n\n\n\nTo do: Output this a dataframe so users can save to csv")
#             # print(ColorPrint.cyan+"You can also print the tests as a dataframe:"+ColorPrint.end)

#             # df = pd.DataFrame(dc.test_results)
#             # print(df)


def run_look_tests(tests_to_run,**kwargs):
    try:
        prod = LookerEnvironment('production',config_instance=kwargs['instance'])
        if not kwargs['single']:
            dev = LookerEnvironment('dev',config_instance=kwargs['instance'])
            dev.checkout_dev_branch(project_name,dev_branch)
    except NameError: 
        print("Error in specifying the instance name, please confirm your argument matches an instance section from the looker.ini file")
    except:
        print("Error in setting the instance configurations")

    if kwargs['single']:
        instances= [prod]
    else:
        instances = [prod,dev]  

    for look_to_test in look_list:   
        if kwargs['single']:
            lc = LookCheckerSingle(look_to_test,kwargs,instances[0],tests_to_run)
            lc.run_tests()
            lc.output_tests()

        else:
            print("Look comparison is under construction, use -s arg to check single")
    


if __name__ == '__main__':
    # Run setup, parses the command line arguments and stores them into a dictionary called kwargs
    args = setup()
    
    # Retrieve a list of configured instances
    instances = config_instances(args)

    # Retrieve a list of tests to run on the instances
    dashboard_tests, look_tests = config_tests()

    # Run tests
    run_tests(dashboard_list,instances,dashboard_tests,look_tests)

    # if len(dashboard_list) > 0 and dashboard_list[0] != "":
    #     # Set the configuration of tests you would like to run on your dashboard
    #     dashboard_to_check = config_dashboard_test('config_tests.ini',**kwargs)

    #     # Run the tests
    #     run_dashboard_tests(dashboard_to_check,**kwargs)
    # else:
    #     print("No dashboards to test")

    # if len(look_list) > 0 and look_list[0] != "":
    #     # Set the configuration of tests you would like to run on your look
    #     look_to_check = config_look_test('config_tests.ini',**kwargs)

    #     # Run the tests
    #     run_look_tests(look_to_check,**kwargs)
    # else:
    #     print("No looks to test")

  