import yaml
import logging
import configparser

# TODO: Add in input sanization methods
def input_sanization():
    pass

# Looker file typically more sensitive
def _read_sections(looker_file):
    config = configparser.ConfigParser()
    file = looker_file
    config.read(file)
    return [key for key in config._sections.keys()]

def add_environment(add_instance:str = 'y',looker_file = "looker.ini"):
    instances = []
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
            proj_branch = proj + "|" + branch
        else:
            proj_branch = "production"

        instances.append([instance,proj_branch ])
        print("Add another instance?")
        
        loop = input("->Y|N: ")
        if loop.lower() != "y":
            add_instance = 'n'

    logging.info(f"Number of instances {instances}")
    return instances