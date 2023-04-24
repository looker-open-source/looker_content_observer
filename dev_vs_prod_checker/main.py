from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
from dashboardchecker import DashboardChecker
import configparser
import argparse
from colorprint import ColorPrint
import pandas as pd

dashboard_to_test = "jhu_covid::jhu_base_template_extend"
# dashboard_to_test = "5"
# dashboard_to_test = "2"

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

    # Dashboard Checks 
    dashboard_checks = []
    for test,run_test in config._sections['Dashboard'].items():
        if run_test.lower() == "true":
            dashboard_checks.append(test)
    return dashboard_checks


def run_tests(check_test):
    try:
        prod = LookerEnvironment('production',config_instance=instance)
        dev = LookerEnvironment('dev',config_instance=instance)
        dev.checkout_dev_branch(project_name,dev_branch)
    except NameError: 
        print("Error in specifying the instance name, please confirm your argument matches an instance section from the looker.ini file")
    except:
        print("Error in setting the instance configurations")

    instances = [prod,dev]   
    dc = DashboardChecker(dashboard_to_test,*instances,check_test)
    
    
    tests = [
            #dc.unit_test_number_of_dashboard_elemets,
            # dc.data_test_tile_match,
            dc.parse_dashboard
             ]

    for test in tests:
        test()
 
    dc.output_tests()

    print("\n\n\n\nTo do: Output this a dataframe so users can save to csv")
    print(ColorPrint.cyan+"You can also print the tests as a dataframe:"+ColorPrint.end)
    # for test_record in dc.test_results:
    #     print(test_record)

    # print(dc.tests_to_run)
    # print(ColorPrint.green+"\nOutput of an example csv/dataframe of the results and an example test:"+ColorPrint.end)
    
    df = pd.DataFrame(dc.test_results)
    print(df)
    # df = df.T
    # df.columns = df.iloc[0]
    # df['is_match'] = df.iloc[:,0] == df.iloc[:,1] 
    # print(df.iloc[1:,:])

    # df.to_csv("output_of_test_results.csv",index=False)

if __name__ == '__main__':
    # Set instance configs
    instance, dev_branch, project_name = config_instance()
    
    # run_tests()
    dashboard_checks = config_test('config_tests.ini')

    run_tests(dashboard_checks)