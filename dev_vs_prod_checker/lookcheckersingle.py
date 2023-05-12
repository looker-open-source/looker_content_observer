from look import Look
from colorprint import ColorPrint
from looktest import LookTest
import pandas
class LookCheckerSingle(Look):
    def __init__(self, look_id,kwargs,instance_1:object, tests_to_run:list) -> None:
        super().__init__(look_id,kwargs)
        self.test_results = []
        self.instance_1 = instance_1
        self.instances = [self.instance_1]
        self.tests_to_run = tests_to_run
        self.api_methods = ['get_look_data']
    
    def run_tests(self) -> None:
        """
        :overview:
        - Runs a Test (from the Test class) on a look in one instance
        - Stores the test result within the self.test_results parameter

        :returns: 
        - None
        """
        for instance in self.instances:
            look = self.get_look(instance.sdk)
            for method_to_test in self.tests_to_run:
                output = {}
                output['instance_environment'] = instance.config_instance + "." + instance.environment # Output: LookerUAT.production or LookerProd.dev 
                output['look_title'] = look.title # look Title
                print("Testing Look " + look.id + ": " + look.title + " - on " + output['instance_environment'])
                
                if method_to_test in self.api_methods: # Certain methods will need to make an additional API call
                    output[method_to_test] = getattr(LookTest,method_to_test)(look,instance.sdk)
                    if self.kwargs['logging']:
                        print("Start Logging" + "." * 100)
                        print("Checking the number of length of the output dict:",len(output[method_to_test]), f"for following test:{method_to_test}")
                        print("End Logging" +  "." * 100)
                else:
                    output[method_to_test] = getattr(LookTest,method_to_test)(look)
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
        - create a method to confirm if the number of visualization tiles are the same 
        - create a method to confirm the position of the tiles (based on id?) is the same
        - confirm behavior of API if query_id does not exist
        """
        print(ColorPrint.underline + "Outputting Look Level Tests:" + ColorPrint.end)
        for method_to_test in self.tests_to_run:
            combined_test = []
            for test_ouput in self.test_results:
                # Check to confirm if names of the tests are the same
                # Example of keys: dict_keys(['instance_environment', 'look_title', 'get_tile_data'])
                if method_to_test in test_ouput.keys():
                    combined_test.append(test_ouput)
            
            instances_name_a = combined_test[0]['instance_environment']
            instance_test_a = combined_test[0][method_to_test]       
            

            print("\nRunning" +
                ColorPrint.blue + f" {method_to_test} " + ColorPrint.end +
                "test between: " + ColorPrint.yellow + f"{instances_name_a}" +  ColorPrint.end )
            # Certain methods involve an extra API Call which will further nest the data
            if method_to_test in self.api_methods:
                
                # TODO: List currently goes off the length of tiles in instance_a, need to update to add a check if both instances are generating X number of visualization tiles
                for df_output_dict in range(len(combined_test[0][method_to_test])):
                    title_a = instance_test_a[df_output_dict]['look_title']
                    #TODO: doesn't handle non query tiles e.g. text or button
                    try:
                        print(ColorPrint.cyan+f"Checking tile number {df_output_dict + 1}: "+title_a+ColorPrint.end) 
                    except:
                        print(ColorPrint.cyan + "Checking a tile" + ColorPrint.end)
                    
                    print(f"\n-->Checking: Was query run succesfully")
                    data_a = instance_test_a[df_output_dict]['df']
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
