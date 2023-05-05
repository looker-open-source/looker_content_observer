# Overview


## How to Run
1. Set up instances in /dev_vs_prod_checker/config.ini (see example looker_ini_file_example.ini for more details)
2. Configure dashboards to run in the `dashboard_list` variable in main.py
3. Choose tests in config_tests.ini
4. Run the following from /dev_vs_prod_checker/ folder

```
python3 main.py -i <instance_name> 
```
where "instance_name" is the name set in config.ini

### Args
```
Specifies the instance

options:
  -h, --help            show this help message and exit
  --instance INSTANCE, -i INSTANCE
                        Name of instance, as defined by the section within the looker.ini file
```