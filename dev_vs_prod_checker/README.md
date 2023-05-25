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
                         ->multiple instances should be space separated, ex: -i GCP_Dev  GCP_UAT GCP_PROD
  --environment -e      Name of environment, choices are either production or dev: 
                        ->example: dev dev production -> each environment maps to the instance, i.e. the first 'dev' maps to the GCP_Dev instance, the second maps to the GCP_UAT instance, and the third element 'production' maps to the GCP_Prod instance

  --loglevel            Choices are: [{DEBUG,INFO,WARNING,ERROR,CRITICAL}], the lower the level in logging, i.e. DEBUG or Info the more verbose the logs.
                        ->Recommendation is try with INFO first.
  --csv [CSV]           Store Data as a CSV, input as, for example, --csv "all_tests_output.csv"
```
