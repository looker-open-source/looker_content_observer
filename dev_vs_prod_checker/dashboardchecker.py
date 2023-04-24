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
