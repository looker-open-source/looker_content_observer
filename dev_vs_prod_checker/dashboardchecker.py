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
    
    def get_data_for_test(self) -> list[pandas.DataFrame]:
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

    def output_tests(self) -> pandas.DataFrame:
        """
        :overview:
        - Retrieves results from the run_tests() method that are stored within the self.test_results attribute
        - Logs/Prints the results to the command line and then outputs a pandas dataframe all results

        :returns: 
        - pandas dataframe of all results

        :to do:
        - Create some helper methods for formatting so not all print statements needed to be so explicitly formatted
        - create a method to confirm if the number of visualization tiles are the same 
        - create a method to confirm the position of the tiles (based on id?) is the same
        - confirm behavior of API if query_id does not exist
        """
        print(ColorPrint.underline + "Outputting Dashboard Level Tests:" + ColorPrint.end)
        for method_to_test in self.tests_to_run:
            combined_test = []
            for test_ouput in self.test_results:
                # Check to confirm if names of the tests are the same
                # Example of keys: dict_keys(['instance_environment', 'dashboard_title', 'get_tile_data'])
                if method_to_test in test_ouput.keys():
                    combined_test.append(test_ouput)
            
            instances_name_a, instances_name_b = combined_test[0]['instance_environment'], combined_test[1]['instance_environment']
            instance_test_a, instance_test_b = combined_test[0][method_to_test], combined_test[1][method_to_test]       
            

            print("\nRunning" +
                ColorPrint.blue + f" {method_to_test} " + ColorPrint.end +
                "test between: " + ColorPrint.yellow + f"{instances_name_a}" +  ColorPrint.end + " vs. " + 
                ColorPrint.cyan + f"{instances_name_b}" + ColorPrint.end)
            # print(dash.title)
            # Certain methods involve an extra API Call which will further nest the data
            if method_to_test in self.api_methods:
                # TODO: List currently goes off the length of tiles in instance_a, need to update to add a check if both instances are generating X number of visualization tiles
                for df_output_dict in range(len(combined_test[0][method_to_test])):
                    title_a, title_b = instance_test_a[df_output_dict]['tile_title'],instance_test_b[df_output_dict]['tile_title']
                    #TODO: doesn't handle non query tiles e.g. text or button
                    print(ColorPrint.cyan+f"Checking tile number {df_output_dict + 1}: "+title_a+ColorPrint.end) 
                    
                    print(f"\n-->Checking: Was query run succesfully")
                    data_a, data_b = instance_test_a[df_output_dict]['df'],instance_test_b[df_output_dict]['df']
                    try:
                        data_a.looker_error #need to think of a better way to test this, prints "Name: looker_error, dtype: object" unnecessarily
                    except:
                        output = True
                    else:
                        output = False
                    if output:
                        print("-->Result:" + ColorPrint.green + " PASS " + ColorPrint.end)
                    else: 
                        print("-->Result:" + ColorPrint.red + " FAIL " + data_a.looker_error + ColorPrint.end)
#####################
####Extra tests #####
            #         print(f"\n-->Checking: If API was succesfully able to run query_id")
            #         has_data = lambda bool_a, bool_b: (bool_a == False) and (bool_b == False)  
            #         api_a, api_b = instance_test_a[df_output_dict]['could_get_api_data'],instance_test_b[df_output_dict]['could_get_api_data']
            #         output = has_data(api_a,api_b) 
            #         if output:
            #             print("-->Result:" + ColorPrint.green + " PASS " + f"Check: {output}" + ColorPrint.end)
            #         else: 
            #             print("-->Result:" + ColorPrint.red + " FAIL " + f"Check: {output}" + ColorPrint.end)

            #         print(f"\n-->Checking: Name of Tiles Match")
            #         title_a, title_b = instance_test_a[df_output_dict]['tile_title'],instance_test_b[df_output_dict]['tile_title']
            #         output = Test.is_equal(title_a,title_b)
            #         if output:
            #             print("-->Result:" + ColorPrint.green + " PASS " + f"Check:'{title_a}'=='{title_b}'" + ColorPrint.end)
            #         else: 
            #             print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:'{title_a}'!='{title_b}'" + ColorPrint.end)
                        
            #         print(f"\n-->Checking: Number of (Row,Columns) of Tile")
            #         shape_a, shape_b = instance_test_a[df_output_dict]['shape'],instance_test_b[df_output_dict]['shape']
            #         output = Test.is_equal(shape_a, shape_b)
            #         if output:
            #             print("-->Result:" + ColorPrint.green + " PASS " + f"Check:'{shape_a}'=='{shape_b}'" + ColorPrint.end)
            #         else: 
            #             print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:'{shape_a}'!='{shape_b}'" + ColorPrint.end)

            #         print(f"\n-->Checking: Tile has Data")
            #         has_data = lambda bool_a, bool_b: (bool_a == False) and (bool_b == False)  
            #         is_empty_a, is_empty_b = instance_test_a[df_output_dict]['is_empty'],instance_test_b[df_output_dict]['is_empty']
            #         output = has_data(is_empty_a,is_empty_b) 
            #         if output:
            #             print("-->Result:" + ColorPrint.green + " PASS both dataframes contain data" + ColorPrint.end)
            #         else: 
            #             print("-->Result:" + ColorPrint.red + " FAIL one or both dataframes are empty" + ColorPrint.end)

            #         print(f"\n-->Checking: Data Between Tiles Is Equal")
            #         data_a, data_b = instance_test_a[df_output_dict]['df'],instance_test_b[df_output_dict]['df']
            #         output = Test.is_dataframe_equal(data_a,data_b)
            #         if output:
            #             print("-->Result:" + ColorPrint.green + " PASS data from dataframes identical" + ColorPrint.end)
            #         else: 
            #             print("-->Result:" + ColorPrint.red + " FAIL data from dataframes not-identical" + ColorPrint.end)

            # else:                    
            #     output = Test.is_equal(instance_test_a,instance_test_b)
            
            #     if output:
            #         print("-->Result:" + ColorPrint.green + " PASS " + f"Check:{instance_test_a}=={instance_test_b}" + ColorPrint.end)
            #     else: 
            #         print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:{instance_test_a}!={instance_test_b}" + ColorPrint.end)
########################