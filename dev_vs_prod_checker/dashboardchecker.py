from dashboard import Dashboard

class DashboardChecker(Dashboard):
    def __init__(self, dashboard_id) -> None:
        super().__init__(dashboard_id)
        self.test_results = []

    def test_output(self,test_name,test_a,test_b,result):
        output = {"test_name":test_name,
                "instance_1":test_a, 
                "instance_2":test_b, 
                "test_result":result,
                }
        return output

    def is_number_equal(self,a,b) -> bool:
        return a == b
    
    def is_dataframes_equal(self,a,b) -> bool:
        return a.equals(b)
        
    def unit_test_number_of_dashboard_elemets(self,instance_1:object,instance_2:object):
        test_a = len(self.get_all_dashboard_elements(instance_1))
        test_b = len(self.get_all_dashboard_elements(instance_2))
        result = self.is_number_equal(test_a,test_b)
        self.test_results.append(self.test_output("unit_test_number_of_dashboard_elemets",test_a,test_b,result))

    def data_test_tile_match(self,instance_1:object,instance_2:object):
        # For now assume the tiles are ordered correctly
        tiles_a = self.get_all_tiles_data(instance_1)
        tiles_b = self.get_all_tiles_data(instance_2)

        for tile_index in range(len(tiles_a)):
            test_a = type(tiles_a[tile_index])
            test_b = type(tiles_b[tile_index])
        
            # result = self.is_dataframes_equal(tiles_a[tile_index],tiles_b[tile_index])
            result = self.is_number_equal(test_a,test_b)
            self.test_results.append(self.test_output("data_test_tile_match",test_a,test_b,result))
