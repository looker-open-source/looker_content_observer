from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
from dashboardchecker import DashboardChecker
import configparser
import argparse
import pandas as pd

# dashboard_to_test = "jhu_covid::jhu_base_template_extend"
dashboard_to_test = "5"

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

if __name__ == '__main__':
    # Set instance configs
    instance, dev_branch, project_name = config_instance()

    # Connect to instances / Instantiate the dev and prod sdks
    try:
        prod = LookerEnvironment('production',config_instance=instance)
        dev = LookerEnvironment('dev',config_instance=instance)
        dev.checkout_dev_branch(project_name,dev_branch)
    except NameError: 
        print("Error in specifying the instance name, please confirm your argument matches an instance section from the looker.ini file")
    except:
        print("Error in setting the instance configurations")

    dc = DashboardChecker(dashboard_to_test)
    instance_sdks = [prod.sdk,dev.sdk]   
        
    tests = [dc.unit_test_number_of_dashboard_elemets,
             dc.data_test_tile_match
             ]
    
    for test in tests:
        test(*instance_sdks)
    
    print(dc.test_results)

    df = pd.DataFrame(dc.test_results)
    print(df)

    df.to_csv("output_of_test_results.csv",index=False)