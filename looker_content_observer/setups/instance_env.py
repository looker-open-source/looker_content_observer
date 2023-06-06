import yaml
import logging
import configparser
import os.path

# TODO: Add in input sanization methods
def input_sanization():
    pass

# Looker file typically more sensitive
def _read_sections(looker_file:os.path) -> list:
    config = configparser.ConfigParser()
    file = looker_file
    config.read(file)
    return [key for key in config._sections.keys()]

def add_environment(add_instance:str = 'y',looker_file = "looker.ini") -> list:
    instances = []

    # Check if looker ini file exists
    try: 
        assert os.path.exists(looker_file),f"Looker ini file does not exist"
        logging.debug(f"Looker ini file found at: {looker_file}")
    except AssertionError:
        print("Could not find looker.ini file (or equivalent)")
        print("Please either create looker.ini file, or specify path to file using -f option")
        exit()
    
    # Check if the Looker ini file has sections configured    
    try:
        sections = _read_sections(looker_file)
        assert len(sections) > 0, f"No sections found"
    except:
        logging.info(f"Sections from _read_sections(): {sections}")
        print("No looker.ini (or equivalent) configuration file found, please create one first before using tool")
        exit()
    
    print("Enter section name for Looker Instance")
    print("Note: Section name comes from the looker.ini file.")
    print("Current section names are:",sections)

    # TODO: Add link to documentation for an example
    while add_instance == 'y':
        try:
            instance = input("->Instance: ")
            assert instance in sections, f"Please enter a valid section"
        except AssertionError:
            logging.debug(f"Instance entered:{instance}")
            print("Instance entered does not match a valid Looker section")
            continue
            
        print("Environment, [1]=production,[2]=development:")
        env = input("->1|2: ")
        assert env in ['1','2'], f"Please enter a valid number"

        if env == '2': 
            print("Please enter the Looker project assosciated with the dashboard")
            proj = input("->Project: ")

            print("Please enter the branch assosciated with the dashboard")
            branch = input("->Branch: ")
            proj_branch = proj + "::" + branch
        else:
            proj_branch = "production"

        instances.append((instance,proj_branch ))
        print("Add another instance?")
        
        loop = input("->Y|N: ")
        if loop.lower() != "y":
            add_instance = 'n'

    logging.info(f"Instances {instances}")
    logging.info("Writing instances to environment_setup.yaml file")
    return instances

def create_instance_yaml(instances:list) -> yaml:
    # Format list of tuples into a dictionary for easier loading to YAML File
    instance_dict = {}
    format_instance_list = lambda format_instance: { "environment": 'dev' if format_instance[1] != 'production' else 'production',
                                "project": str(format_instance[1].split("::")[0]) if format_instance[1] != 'production' else None,
                                "branch": str(format_instance[1].split("::")[1]) if format_instance[1] != 'production' else None, 
                            }
    # Each instance (dict key) will have payload of instance environment, project, and branch
    for instance in instances: 
        instance_dict[instance[0]] = format_instance_list(instance)
    
    with open("configs/instance_environment_configs.yaml","w") as file:
        yaml_file = yaml.dump(instance_dict,file) 

    logging.info("Created the instance + environment configuration file")    