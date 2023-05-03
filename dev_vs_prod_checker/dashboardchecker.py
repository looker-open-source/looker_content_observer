from dashboard import Dashboard
from colorprint import ColorPrint
from test import Test
import pandas
class DashboardChecker(Dashboard):
    def __init__(self, dashboard_id,kwargs,instance_1:object,instance_2:object, tests_to_run:list) -> None:
        super().__init__(dashboard_id,kwargs)
        self.test_results = []
        self.instance_1 = instance_1
        self.instance_2 = instance_2
        self.instances = [self.instance_1,self.instance_2]
        self.tests_to_run = tests_to_run
        self.api_methods = ['get_tile_data']
    
    def run_tests(self) -> None:
        """
        :overview:
        - Runs a Test (from the Test class) on a dashboard between instances
        - Stores the test result within the self.test_results parameter

        :returns: 
        - None
        """
        for instance in self.instances:
            dash = self.get_dashboard(instance.sdk)
            for method_to_test in self.tests_to_run:
                output = {}
                output['instance_environemnt'] = instance.config_instance + "." + instance.environment # Output: LookerUAT.production or LookerProd.dev 
                output['dashboard_title'] = dash.title # Dashboard Title
                if method_to_test in self.api_methods: # Certain methods will need to make an additional API call
                    output[method_to_test] = getattr(Test,method_to_test)(dash,instance.sdk)
                else:
                    output[method_to_test] = getattr(Test,method_to_test)(dash)
                self.test_results.append(output)

    def output_tests(self) -> pandas.DataFrame:
        """
        :overview:
        - Retrieves results from the run_tests() method that are stored within the self.test_results attribute
        - Logs/Prints the results to the command line and then outputs a pandas dataframe all results

        :returns: 
        - pandas dataframe of all results

        :to do:
        - Create some helper methods for formatting so not all print statements needed to be so explicitly formatted
        """
        print(ColorPrint.underline + "Outputting Dashboard Level Tests:" + ColorPrint.end)
        for method_to_test in self.tests_to_run:
            combined_test = []
            for test_ouput in self.test_results:
                if method_to_test in test_ouput.keys():
                    combined_test.append(test_ouput)
            
            instances_name_a, instances_name_b = combined_test[0]['instance_environemnt'], combined_test[1]['instance_environemnt']
            instance_test_a, instance_test_b = combined_test[0][method_to_test], combined_test[1][method_to_test]       
            
            if self.kwargs['logging']:
                print("Start Logging" + "." * 100)
                print("Length of each instance list:")
                print(len(instances_name_a),len(instances_name_b))
                print("End Logging" +  "." * 100)

            print("\nRunning" +
                ColorPrint.blue + f" {method_to_test} " + ColorPrint.end +
                "test between: " + ColorPrint.yellow + f"{instances_name_a}" +  ColorPrint.end + " vs. " + 
                ColorPrint.cyan + f"{instances_name_b}" + ColorPrint.end)

            if method_to_test == 'get_tile_data':
                for df_output_dict in range(len(combined_test)):
                    print(ColorPrint.cyan+f"Checking tile numebr:{df_output_dict}"+ColorPrint.end)

                    print(f"\n-->Checking: Name of Tiles Match")
                    title_a, title_b = instance_test_a[df_output_dict]['tile_title'],instance_test_b[df_output_dict]['tile_title']
                    output = Test.is_equal(title_a,title_b)
                    if output:
                        print("-->Result:" + ColorPrint.green + " PASS " + f"Check:'{title_a}'=='{title_b}'" + ColorPrint.end)
                    else: 
                        print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:'{title_a}'!='{title_b}'" + ColorPrint.end)
                        
                    print(f"\n-->Checking: Number of (Row,Columns) of Tile")
                    shape_a, shape_b = instance_test_a[df_output_dict]['shape'],instance_test_b[df_output_dict]['shape']
                    output = Test.is_equal(shape_a, shape_b)
                    if output:
                        print("-->Result:" + ColorPrint.green + " PASS " + f"Check:'{shape_a}'=='{shape_b}'" + ColorPrint.end)
                    else: 
                        print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:'{shape_a}'!='{shape_b}'" + ColorPrint.end)

                    print(f"\n-->Checking: Tile has Data")
                    has_data = lambda bool_a, bool_b: (bool_a == False) and (bool_b == False)  
                    is_empty_a, is_empty_b = instance_test_a[df_output_dict]['is_empty'],instance_test_b[df_output_dict]['is_empty']
                    output = has_data(is_empty_a,is_empty_b) 
                    if output:
                        print("-->Result:" + ColorPrint.green + " PASS both dataframes contain data" + ColorPrint.end)
                    else: 
                        print("-->Result:" + ColorPrint.red + " FAIL one or both dataframes are empty" + ColorPrint.end)

                    print(f"\n-->Checking: Data Between Tiles Is Equal")
                    data_a, data_b = instance_test_a[df_output_dict]['df'],instance_test_b[df_output_dict]['df']
                    output = Test.is_dataframe_equal(data_a,data_b)
                    if output:
                        print("-->Result:" + ColorPrint.green + " PASS data from dataframes identical" + ColorPrint.end)
                    else: 
                        print("-->Result:" + ColorPrint.red + " FAIL data from dataframes not-identical" + ColorPrint.end)

            else:                    
                output = Test.is_equal(instance_test_a,instance_test_b)
            
                if output:
                    print("-->Result:" + ColorPrint.green + " PASS " + f"Check:{instance_test_a}=={instance_test_b}" + ColorPrint.end)
                else: 
                    print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:{instance_test_a}!={instance_test_b}" + ColorPrint.end)
