from dashboard import Dashboard
from colorprint import ColorPrint
from test import Test
from tile import Tile
import pandas as pd
from functools import reduce
import logging
import pandas

class DashboardChecker(Dashboard):
    def __init__(self, dashboard_id:str,instances:list,tests_to_run:dict) -> None:
        super().__init__(dashboard_id)
        self.test_results = [] # List of dictionary items
        self.instances = instances
        # Contains both dashboard level and tile level tests
        self.tests_to_run = tests_to_run
        self.dashboard_level_tests:list = list(filter(lambda run_test: self.tests_to_run['dashboard_level'][run_test] == True,self.tests_to_run['dashboard_level'])) 
        self.tile_level_tests:list = list(filter(lambda run_test: self.tests_to_run['tile_level'][run_test] == True,self.tests_to_run['tile_level']))
    
    def get_data_for_test(self) -> list:
        """
        - Method largely makes API calls to retrive data to be later used in testing + comparisons
        - Certain methods require multiple API calls, these are specified in the self.api_methods
        - Data is formatted as a dictionary and then appended to self.test_results
        - :returns: dictionary
        """
        instance_dfs = []
        for instance in self.instances:
            output = []
            logging.info(ColorPrint.yellow + f"Runnings tests on following instances: {instance.config_instance}" + ColorPrint.end)
            dash = self.get_dashboard(instance.sdk)
            instance_environment = instance.config_instance + "." + instance.environment
            # Run dashboard level tests
            for method_to_test in self.dashboard_level_tests:
                logging.info(ColorPrint.yellow + f"Runnings tests on following method: {method_to_test}" + ColorPrint.end)
                # Check if test is set to true
                result_from_test = getattr(Test,method_to_test)(dash)
                output.append([instance_environment,dash.title,"dashboard",method_to_test,result_from_test])  

            # Run tile level tests
            logging.info(ColorPrint.yellow + f"Runnings tile level tests: {self.tile_level_tests}" + ColorPrint.end)
            for element in dash.dashboard_elements:
                t = Tile(element,dash.dashboard_layouts,instance.sdk)
                for tile_method_to_test in self.tile_level_tests:
                    # Check if test is set to true
                    result_from_test = getattr(Test,tile_method_to_test)(t)
                    logging.debug(ColorPrint.blue + f"Result from test: {result_from_test} for test-{tile_method_to_test}" + ColorPrint.end)
                    # if key exists
                    output.append([instance_environment,dash.title,f"tile-{t.tile_pkey}",tile_method_to_test,result_from_test])     
            instance_dfs.append(pd.DataFrame(output,columns =['instance_environment','dashboard_title','level','test','test_result']))

        # Merge, via outer join, the dataframes together
        if len(instance_dfs) > 1:
            combined = reduce(lambda left,right: pd.merge(left, right, on=['dashboard_title','level','test'], how='outer'), [*instance_dfs])
            instance_dfs.append(combined[sorted(combined.columns)])
                
        return instance_dfs[-1] 