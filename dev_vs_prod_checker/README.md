# Overview


## How to Run
1. Set up instances in /dev_vs_prod_checker/looker.ini (see example looker_ini_file_example.ini for more details)
2. Configure dashboards to run in the `dashboard_list` variable in main.py
3. Choose tests in config_tests.ini
4. Run the following from /dev_vs_prod_checker/ folder

```
python3 main.py -i GCP234 VM VM -e dev dev production -l DEBUG --csv "test.csv"    
```
where "instance_name" is the name set in config.ini

### Args
```
Specifies the instance

options:
  -h, --help            show this help message and exit
  --instance -i         Name of instances, names must match the looker.ini sections: 
                        ->multiple instances should be space separated, ex: -i DEV UAT PROD
  --environment -e    Name of environment, choices are either production or dev: 
                        ->example: dev dev dev -> wuld run the code for each instance from the branch specified within the looker.ini file for each dev uat and prod instance

  --loglevel [{DEBUG,INFO,WARNING,ERROR,CRITICAL}], -l [{DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        set the logging level
  --single, -s          Run on a single instance+branch only
  --csv [CSV]           Store Data as a CSV
```
