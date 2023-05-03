from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
from dashboardchecker import DashboardChecker
import configparser
import argparse
from colorprint import ColorPrint
import pandas as pd

dashboard_to_test = "jhu_covid::jhu_base_template_extend"
# dashboard_to_test = "5"
# dashboard_to_test = "13"

def config_instance():
    # Specify the instance to connect to from the argparse
    parser = argparse.ArgumentParser(description='Arg to specify the instance to connect to.')
    parser.add_argument('--instance', '-i', help='Name of instance, as defined by the section within the looker.ini file')
    args = parser.parse_args()

    # looker.ini file will have the configurations to specify the branch and project
    config = configparser.ConfigParser()
    config_file = "looker.ini"
    config.read(config_file)
    dev_branch = config[args.instance]['dev_branch']
    project_name = config[args.instance]['project']
    return args.instance, dev_branch,project_name    

def config_test(path_to_config_file):
    config = configparser.ConfigParser()
    file = path_to_config_file
    config.read(file)
    # Checks sections within checks config file
    # print(config._sections)
    tests_to_run = []
    for test,run_test in config._sections['Dashboard'].items():
        if run_test.lower() == "true":
            tests_to_run.append(test)
    return tests_to_run


def run_tests(tests_to_run):
    try:
        prod = LookerEnvironment('production',config_instance=instance)
        dev = LookerEnvironment('dev',config_instance=instance)
        dev.checkout_dev_branch(project_name,dev_branch)
    except NameError: 
        print("Error in specifying the instance name, please confirm your argument matches an instance section from the looker.ini file")
    except:
        print("Error in setting the instance configurations")

    instances = [prod,dev]   
    dc = DashboardChecker(dashboard_to_test,*instances,tests_to_run)
        
    # to do: create a dc.run_tests method
    # Step 1: Run the tests
    dc.run_tests()

    # Step 2: Log and print out the outputs
    dc.output_tests()

    # Step 3: Output a dataframe we can turn into a CSV
    print("\n\n\n\nTo do: Output this a dataframe so users can save to csv")
    print(ColorPrint.cyan+"You can also print the tests as a dataframe:"+ColorPrint.end)

    df = pd.DataFrame(dc.test_results)
    print(df)


if __name__ == '__main__':
    # Set instance configs
    instance, dev_branch, project_name = config_instance()
    
    # Set the configuration of tests you would like to run on your dashboard
    dashboard_to_check = config_test('config_tests.ini')

    # Run the tests
    run_tests(dashboard_to_check)