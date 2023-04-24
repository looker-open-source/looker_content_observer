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

    def format_output(self,test_name,test_a,test_b,result):
        output = {
                "test_name":test_name,
                "instance_1":test_a, 
                "instance_2":test_b, 
                "test_result":result,
                }
        return output
    
    def parse_dashboard(self):
        for instance in self.instances:
            dash = self.get_dashboard(instance.sdk)

            for method_to_test in self.tests_to_run:
                output = {}
                output['instance_environemnt'] = instance.config_instance + "." + instance.environment # Output: LookerUAT.production or LookerProd.dev 
                output['dashboard_title'] = dash.title # Dashboard Title
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
            
            output = Test.is_equal(instance_test_a,instance_test_b)
            
            if output:
                print("-->Result:" + ColorPrint.green + " PASS " + f"Check:{instance_test_a}=={instance_test_b}" + ColorPrint.end)
            else: 
                print("-->Result:" + ColorPrint.red + " FAIL " + f"Check:{instance_test_a}!={instance_test_b}" + ColorPrint.end)

    def unit_test_number_of_dashboard_elemets(self):
        test_a = len(self.get_all_dashboard_elements(self.instance_1.sdk))
        test_b = len(self.get_all_dashboard_elements(self.instance_2.sdk))
        result = self.test.is_equal(test_a,test_b)
        output = self.format_output("unit_test_number_of_dashboard_elemets",test_a,test_b,result)
        self.test_results.append(output)

    def data_test_tile_match(self):
        # For now assume the tiles are ordered correctly
        tiles_a = self.get_all_tiles_data(self.instance_1.sdk)
        tiles_b = self.get_all_tiles_data(self.instance_2.sdk)

        for tile_index in range(len(tiles_a)):
            test_a = type(tiles_a[tile_index])
            test_b = type(tiles_b[tile_index])
        
            # result = self.is_dataframes_equal(tiles_a[tile_index],tiles_b[tile_index])
            result = self.test.is_equal(test_a,test_b)
            output = self.format_output("data_test_tile_match",test_a,test_b,result)
            self.test_results.append(output)
