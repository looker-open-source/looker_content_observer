from _lco.look import Look
from _lco.colorprint import ColorPrint
from _lco.test import Test
import pandas as pd
from functools import reduce
import logging

class LookChecker(Look):
    def __init__(self, look_id:str,instances:list,tests_to_run:dict) -> None:
        super().__init__(look_id)
        self.test_results = [] # List of dictionary items
        self.instances = instances
        # Contains both dashboard level and tile level tests
        self.tests_to_run = tests_to_run
        # self.look_level_tests:list = self.tests_to_run['look_tests']
        self.look_level_tests:list = list(filter(lambda item:  item[1] == True,self.tests_to_run.items()))

    
    def get_data_for_test(self) -> list:
        """
        - Method largely makes API calls to retrive data to be later used in testing + comparisons
        - Certain methods require multiple API calls, these are specified in the self.api_methods
        - Data is formatted as a dictionary and then appended to self.test_results
        - :returns: dictionary
        """
        logging.debug(ColorPrint.blue + f"Starting Look level checks: {self.look_level_tests}" + ColorPrint.end)
        instance_dfs = []
        for instance in self.instances:
            output = []
            logging.info(ColorPrint.yellow + f"Sending request to return detailed information about a Look and its associated Query." + ColorPrint.end)
            look = self.get_look(instance.sdk)
            instance_environment = instance.config_instance + "." + instance.environment
            # Run dashboard level tests
            for method_to_test, bool_val in self.look_level_tests:
                logging.info(ColorPrint.yellow + f"Runnings tests on following method: {method_to_test}" + ColorPrint.end)
                # Check if test is set to true
                result_from_test = getattr(Test,method_to_test)(look)
                output.append([instance_environment,
                               look.title,
                               "look",
                               method_to_test,
                               result_from_test,
                               ])  

            instance_dfs.append(pd.DataFrame(output,
                                             columns =['instance_environment','dashboard_title','level','test','test_result'],
                                            ))

        # Merge, via outer join, the dataframes together
        if len(instance_dfs) > 1:
            combined = reduce(lambda left,right: pd.merge(left, right, on=['dashboard_title','level','test'], how='outer'), [*instance_dfs])
            instance_dfs.append(combined[sorted(combined.columns)])
                
        return instance_dfs[-1] 