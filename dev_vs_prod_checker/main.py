from lookerenvironment import LookerEnvironment
from dashboard import Dashboard
import configparser


if __name__ == '__main__':
    # Set the branch and project
    config = configparser.ConfigParser()
    # Turn into argparse
    config_file = "looker.ini"
    config.read(config_file)
    dev_branch = config['VM']['dev_branch']
    project_name = config['VM']['project']
    