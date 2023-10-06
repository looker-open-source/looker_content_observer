# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _lco.look import Look
from _lco.colorprint import ColorPrint
from _lco.test import Test
from pandas import DataFrame,merge
from functools import reduce
from json import dumps
from time import monotonic
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
        - Makes API calls to retrive data to be later used in testing + comparisons
        - Certain tests require multiple API calls, these are specified in the self.api_methods
        - :returns: list containing pandas dataframe
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
                metadata = {"runtime":0}
                start_time = monotonic()
        
                logging.info(ColorPrint.yellow + f"Runnings tests on following method: {method_to_test}" + ColorPrint.end)
                # Check if test is set to true
                result_from_test = getattr(Test,method_to_test)(look,instance.sdk)
                duration = monotonic() - start_time                            
                metadata["runtime"] = round(duration,4)
                
                output.append([instance_environment,
                               look.title,
                               "look",
                                str(dumps(metadata)), # Convert dictionary to json string
                               method_to_test,
                               result_from_test,
                               ])  

            instance_dfs.append(DataFrame(output,
                                             columns =['instance_environment',
                                                       'dashboard_title',
                                                       'level',
                                                       'metadata',
                                                       'test',
                                                       'test_result'
                                                       ],
                                            )
                                )

        # Merge, via outer join, the dataframes together
        if len(instance_dfs) > 1:
            combined = reduce(lambda left,right: merge(left, right, on=['dashboard_title','level','test'], how='outer'), [*instance_dfs])
            instance_dfs.append(combined[sorted(combined.columns)])
                
        return instance_dfs[-1] 