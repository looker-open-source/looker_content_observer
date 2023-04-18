from dashboard_validator import LookerEnvironment,Dashboard
from colorprint import ColorPrint
import configparser

def quickstart_check_authentication(instance_name):
    """
    overview: 
    - Function tries to authenticate to an instance and checks if credentials are valid
    - Start here to confirm your API keys are working
    - If succesful, you will see a dictionary of your credentials
    - Quickstart checks the same instance and creates a connections from the production and dev environments 

    args: 
    - instance_name: Comes from the looker.ini file, defined by the section --> See : https://www.promotic.eu/en/pmdoc/Directions/FileFmt/ini/FmtIni.htm
        - For example: from the ../dev_vs_prod_checker/looker_ini_file_example.ini, the section are LookerUAT or LookerProduction    
    returns:
    - sdk.me() -> See: https://github.com/looker-open-source/sdk-codegen/blob/main/python/looker_sdk/sdk/api40/methods.py#L10941
    """    
    # Step 1: Create a production and development environment
    # --> These environments / class instantiations allow us to query the same instance from 2 different 'perspectives'
    # --> I.e. from the perspective of production environment or from the perspective of a development branch
    # 
    # Note: Looker takes in either the string 'production' for production and 'dev' for development 
    prod = LookerEnvironment('production',config_instance=instance_name)
    dev = LookerEnvironment('dev',config_instance=instance_name)

    print(ColorPrint.yellow + "Printing Production Users Credentials:"+ ColorPrint.end + "\n")
    print(prod.me)
    print(ColorPrint.green + "Authentication to production branch of instance, successful." + ColorPrint.green)

    print(ColorPrint.cyan + "\nPrinting Development Users Credentials:"+ ColorPrint.end + "\n")
    print(dev.me)
    print(ColorPrint.green + "Authentication to dev branch of instance, successful." + ColorPrint.green)

if __name__ == "__main__":
    try:
        quickstart_check_authentication('VM')
    except:
        print("There was an error trying to authenticate to your instance. Please check your API keys and/or ")