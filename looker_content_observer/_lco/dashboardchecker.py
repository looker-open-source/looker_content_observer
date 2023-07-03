from _lco.dashboard import Dashboard
from _lco.colorprint import ColorPrint
from _lco.test import Test
from _lco.tile import Tile
from pandas import DataFrame,merge
from time import monotonic
from json import dumps
from functools import reduce
import logging

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
        - Makes API calls to retrive data to be later used in testing + comparisons
        - Certain tests require multiple API calls, these are specified in the self.api_methods
        - :returns: list containing pandas dataframe
        """
        logging.debug(ColorPrint.blue + "Starting dashboard level checks")
        instance_dfs = []
        for instance in self.instances:
            output = []
            logging.info(ColorPrint.yellow + f"Runnings tests on following instances: {instance.config_instance}" + ColorPrint.end)
            dash = self.get_dashboard(instance.sdk)
            instance_environment = instance.config_instance + "." + instance.environment
            # Run dashboard level tests
            for method_to_test in self.dashboard_level_tests:
                # Dictionary to keep track of metadata
                metadata = {"runtime":0}
                start_time = monotonic()

                logging.info(ColorPrint.yellow + f"Runnings tests on following method: {method_to_test}" + ColorPrint.end)
                # Run Test
                result_from_test = getattr(Test,method_to_test)(dash)
                # Capture runtime
                duration = monotonic() - start_time                            
                metadata["runtime"] = round(duration,4)
                # Append results to output list
                output.append([instance_environment,
                               dash.title,
                               "dashboard",
                               str(dumps(metadata)),
                               method_to_test,
                               result_from_test]
                               )  
            # Run tile level tests
            logging.info(ColorPrint.yellow + f"Runnings tile level tests: {self.tile_level_tests}" + ColorPrint.end)
            for element in dash.dashboard_elements:
                t = Tile(element,dash.dashboard_layouts,instance.sdk)
                for tile_method_to_test in self.tile_level_tests:
                    # Dictionary to keep track of metadata
                    metadata = {"runtime":0}
                    start_time = monotonic()
                    # Run Test
                    result_from_test = getattr(Test,tile_method_to_test)(t)
                    logging.debug(ColorPrint.blue + f"Result from test: {result_from_test} for test-{tile_method_to_test}" + ColorPrint.end)
                    # Capture runtime
                    duration = monotonic() - start_time                            
                    metadata['runtime'] = round(duration,4)
                    # Append data to output list
                    output.append([instance_environment,dash.title,f"tile-{t.tile_pkey}",str(dumps(metadata)),tile_method_to_test,result_from_test])     
            instance_dfs.append(DataFrame(output,
                                          columns =['instance_environment',
                                                    'dashboard_title',
                                                    'level',
                                                    'metadata',
                                                    'test',
                                                    'test_result'
                                                    ]
                                        )
                                )

        # Combined multiple dataframes together, logic 'reduces' multiple dataframes down to a single merged final output
        if len(instance_dfs) > 1:
            combined = reduce(lambda left,right: merge(left, right, on=['dashboard_title','level','test'], how='outer'), [*instance_dfs])
            instance_dfs.append(combined[sorted(combined.columns)])
                
        return instance_dfs[-1] 