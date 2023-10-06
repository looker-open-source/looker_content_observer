#License Header

import logging
from _lco.colorprint import ColorPrint
from _lco.lookerenvironment import LookerEnvironment
import os.path
import yaml

def load_instance_env_yaml(instance_env_file_path:str="configs/instance_environment_configs.yaml") -> dict:
    # Check if the file exists in the correct folder path
    try:
        assert os.path.exists(instance_env_file_path),ColorPrint.red + f"Error - File Not Found: Instance + Environment Configuration File not Found. Please run `lco init` first to set up configuration file" + ColorPrint.end
    except AssertionError as file_not_found:
        print(file_not_found)
        exit()

    # Load the file
    print("Loading saved instance+config file configuration file")
    print("File loaded from: configs/instance_environment_configs.yaml")
    with open(instance_env_file_path, "r") as instance_env_file:
        try:
            instance_env_config = yaml.safe_load(instance_env_file)
            logging.info(ColorPrint.yellow + f"Instance + Env Config:{instance_env_config}")
        except yaml.YAMLError as exc:
            print(exc)
    return instance_env_config

def config_tests(path_to_yaml_config_file:str="configs/config_tests.yaml") -> dict:
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


def config_instances(looker_file:str = "looker.ini") -> list:
    """
    - Instantiate each LookerEnvironment class per instance + environment to a list
    :returns: List of instantiated LookerEnvironments
    """
    logging.info(ColorPrint.yellow + "Instantiating instances" + ColorPrint.end)
    # Append each instance as LookerEnvironment class to list
    instance_env_config = load_instance_env_yaml()
    instances = []

    for instance in instance_env_config:
        logging.info(ColorPrint.yellow + f"Starting connection to instance:{instance.get('instance')}, on {instance.get('environment')}" + ColorPrint.end)
        logging.debug(ColorPrint.blue + f"Checking instance payload: {instance}" + ColorPrint.end )
        logging.debug(ColorPrint.blue + f"Checking instance Instance: {instance.get('instance')}" + ColorPrint.end )
        logging.debug(ColorPrint.blue + f"Checking instance Environment: {instance.get('environment')}" + ColorPrint.end )
        instance_to_test = LookerEnvironment(instance.get('environment'), 
                                             config_file=looker_file,
                                             config_instance=instance.get('instance'))
        # If we are testing a dev branch from an instance, we need to first checkout the dev branch in quest
        # Note: the code tested will based on the latest committed code, please commit any code changes prior to running script
        if instance.get('environment') == 'dev':
            # The Looker project and dev branch are configured as keys within the looker.ini (or .ini equivalent file)
            # Checkout dev branch of the instance, dev branch specified in the looker ini file
            logging.debug("Checkout dev branch")
            instance_to_test.checkout_dev_branch(instance.get('project'),
                                                instance.get('branch'))
            logging.info(ColorPrint.green + "Succesfully checked out dev branch" + ColorPrint.end)
        # Append to instance list
        instances.append(instance_to_test)
    return instances