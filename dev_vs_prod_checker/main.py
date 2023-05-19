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
                config = configparser.ConfigParser()
                file = looker_ini_file_path
                config.read(file)
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

def config_dashboard_test(path_to_config_file,**kwargs):
    config = configparser.ConfigParser()
    file = path_to_config_file
    config.read(file)
    # Checks sections within checks config file
    
    tests_to_run = []
    for test,run_test in config._sections['Dashboard'].items():
        if run_test.lower() == "true":
            tests_to_run.append(test)
    return tests_to_run

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
    kwargs = setup()
    
    # Retrieve a list of configured instances
    instances = config_instances(kwargs)


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

  