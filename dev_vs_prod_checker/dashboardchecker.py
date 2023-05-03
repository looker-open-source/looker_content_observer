from dashboard import Dashboard
from colorprint import ColorPrint
from test import Test
class DashboardChecker(Dashboard):
    def __init__(self, dashboard_id,instance_1:object,instance_2:object, tests_to_run:list) -> None:
        super().__init__(dashboard_id)
        self.test_results = []
        self.instance_1 = instance_1
        self.instance_2 = instance_2
        self.instances = [self.instance_1,self.instance_2]
        self.tests_to_run = tests_to_run
        self.api_methods = ['get_tile_data']
    
    def run_tests(self):
        # To do: split this method into mulitple parts
        for instance in self.instances:
            dash = self.get_dashboard(instance.sdk)

            for method_to_test in self.tests_to_run:
                output = {}
                output['instance_environemnt'] = instance.config_instance + "." + instance.environment # Output: LookerUAT.production or LookerProd.dev 
                output['dashboard_title'] = dash.title # Dashboard Title
                if method_to_test in self.api_methods:
                    output[method_to_test] = getattr(Test,method_to_test)(dash,instance.sdk)
                    print(output)
                else:
                    output[method_to_test] = getattr(Test,method_to_test)(dash)
                self.test_results.append(output)

    def output_tests(self):
        """
        - To do: Clean up this output method
        """
        print(ColorPrint.underline + "\nRunning Dashboard Level Tests:" + ColorPrint.end)
        for method_to_test in self.tests_to_run:
            combined_test = []
            for test_ouput in self.test_results:
                if method_to_test in test_ouput.keys():
                    combined_test.append(test_ouput)
            
            instances_name_a, instances_name_b = combined_test[0]['instance_environemnt'], combined_test[1]['instance_environemnt']
            instance_test_a, instance_test_b = combined_test[0][method_to_test], combined_test[1][method_to_test]       
            print("\nRunning" +
                 ColorPrint.blue + f" {method_to_test} " + ColorPrint.end +
                   "test between: " + ColorPrint.yellow + f"{instances_name_a}" +  ColorPrint.end + " vs. " + 
                   ColorPrint.cyan + f"{instances_name_b}" + ColorPrint.end)
            
            # To do: switch output based on if test output is coming from a dataframe or other data type 
            if method_to_test == 'get_tile_data':
                # To do: If query_id is different between instances, how to check if data is the same?
                output = Test.is_dataframe_equal(instance_test_a,instance_test_b)
            else:
                output = Test.is_equal(instance_test_a,instance_test_b)
            
            if output:
                print("-->Result:" + ColorPrint.green + " PASS " + f"Check:{instance_test_a}=={instance_test_b}" + ColorPrint.end)
            else: 
                print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:{instance_test_a}!={instance_test_b}" + ColorPrint.end)
