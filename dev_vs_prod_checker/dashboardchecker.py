from dashboard import Dashboard
from test import Test
class DashboardChecker(Dashboard):
    def __init__(self, dashboard_id,instance_1:object,instance_2:object) -> None:
        super().__init__(dashboard_id)
        self.test_results = []
        self.test = Test() # Instantiate the Test() class
        self.instance_1 = instance_1
        self.instance_2 = instance_2
        self.instances = [self.instance_1,self.instance_2]

    def format_output(self,test_name,test_a,test_b,result):
        output = {"test_name":test_name,
                "instance_1":test_a, 
                "instance_2":test_b, 
                "test_result":result,
                }
        return output
    
    def parse_dashboard(self):
        for instance in self.instances:
            dash = self.get_dashboard(instance.sdk)
            output = {}
            output['instance_environemnt'] = instance.config_instance + "." + instance.environment # Output: LookerUAT.production or LookerProd.dev 
            output['dashboard_title'] = dash.title # Dashboard Title
            output['number_of_elements'] = len(dash.dashboard_elements)
            output['number_of_dashboard_filters'] = len(dash.dashboard_filters)
            output['hash_of_filters'] = hash(frozenset([str(val) for val in sorted(dash.dashboard_filters, key= lambda obj: obj.id)]))
            output['type_of_dashboard'] = 'LookML Dashboard' if dash.lookml_link_id else 'UDD'
            self.test_results.append(output)
        
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
