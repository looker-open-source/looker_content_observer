import pandas as pd
from look import Look
import json

class LookTest:
    def is_equal(a,b) -> bool:
        return a == b
    
    def is_dataframe_equal(a:pd.DataFrame,b:pd.DataFrame) -> bool:
        return a.equals(b)
    
    def get_number_filters_in_look(look):
        return len(look.filters)
    
    def get_hash_of_all_filters(look):
        """
        overview: 
        - Each dashboard element is an object, this method converts the object into a string and then hashes the string and is used in a check to compare hashes
        - Note: This method will likely fail if the id of the dashboard element has changed
        :returns: 
        - Hash of representing all dashboard elemtns
        """
        return hash(frozenset([str(val) for val in sorted(look.look_filters, key= lambda obj: obj.id)]))

    def get_name_of_look(look):
        return look.title
    
    def get_look_data(look,sdk:object):
        dfs = []
        
        name_of_look = look.title
        if name_of_look == None or name_of_look == '':
            name_of_look = "None"
        
        
        if look.query.id is not None: 
            failed_to_get_data = False                
            
            print(look.title)
            print(look.query.id)
            df = pd.read_json(sdk.run_query(query_id=look.query.id,result_format='json'))
            pd.set_option("display.max_colwidth", 1000) #TODO: not the right place for this, but for some reason this is the only place i could get it to work without throwing error "NameError: name 'pd' is not defined"
            output = {'df':df,
                "query_id":look.query.id,
                "is_empty": df.empty,
                "shape":df.shape,
                "look_title":look.title, 
                "could_get_api_data":failed_to_get_data}
            dfs.append(output)
            print("Success (Look)")
            
        else:
            failed_to_get_data = True
            print("Failed to get data from look")
            output = {'df':None,
                "query_id":None,
                "is_empty": None,
                "shape":None,
                "tile_title":look.title, 
                "could_get_api_data":failed_to_get_data}
            dfs.append(output)
            
        return dfs