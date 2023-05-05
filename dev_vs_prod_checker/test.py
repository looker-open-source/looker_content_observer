import pandas as pd
from dashboard import Dashboard
import json

class Test:
    def is_equal(a,b) -> bool:
        return a == b
    
    def is_dataframe_equal(a:pd.DataFrame,b:pd.DataFrame) -> bool:
        return a.equals(b)
    
    def get_number_tiles_in_dash(dash):
        return len(dash.dashboard_elements)
    
    def get_number_filters_in_dash(dash):
        return len(dash.dashboard_filters)
    
    def get_hash_of_all_filters(dash):
        """
        overview: 
        - Each dashboard element is an object, this method converts the object into a string and then hashes the string and is used in a check to compare hashes
        - Note: This method will likely fail if the id of the dashboard element has changed
        :returns: 
        - Hash of representing all dashboard elemtns
        """
        return hash(frozenset([str(val) for val in sorted(dash.dashboard_filters, key= lambda obj: obj.id)]))

    def get_type_of_dashboard(dash):
        # UDD - User defined dashboard
        return 'LookML Dashboard' if dash.lookml_link_id else 'UDD'
    
    def get_hash_of_query_from_dashboard(dash):
        queries = []
        for dash_element in dash.dashboard_elements:
            pass
            # print(dash_element)
        return None
    
    def get_composition_of_dashboard(dash):
        """
        overview: 
        - Tests if a dashboard has the same number of elements by the type of dashboard visualization
        :returns: 
        - Dictionary, sorted by type of dashboards key, with the counts by element
        """
        composition = {}
        for dash_element in dash.dashboard_elements:
            if dash_element.type not in composition:
                composition[dash_element.type] = 1
            else:
                composition[dash_element.type] += 1
        # Sort by keys
        return sorted(composition.items())

    def get_name_of_tile(tile):
        if tile.type == 'button':
            try:
                return json.loads(tile.rich_content_json)['text']
            except: 
                return "Error with parsing JSON of button"
        elif tile.type == 'text':
            return tile.title_text_as_html
        elif tile.type == 'vis':
            return tile.title
        else:
            return "Unmapped"

    def get_tile_names(dash):
        composition = {}
        for tile in dash.dashboard_elements:
            name_of_tile = Test.get_name_of_tile(tile)
            if name_of_tile == None or name_of_tile == '':
                name_of_tile = "None"
            if name_of_tile not in composition:
                composition[name_of_tile] = 1
            else:
                composition[name_of_tile] += 1
        # Sort by keys
        return sorted(composition.items())
    
    def get_tile_data(dash,sdk:object):
        dfs = []
        merge_list = []
        for tile in dash.dashboard_elements:
            # print("Checking............................",Test.get_name_of_tile(tile))
            # print("Type of Tile.........................",tile.type)
            if tile.type == 'vis' or tile.type == 'looker_map':
                if tile.result_maker.query_id is not None: #most vis have a query ID, if they do not it is likely a merge query
                    # result_maker_list.append(tile.result_maker)
                    # print("Length of result maker is",len(tile.result_maker))
                    # for result_maker in result_maker_list:
                    # print("QueryID from result maker is",tile.result_maker.query_id)
                    failed_to_get_data = False                
                    try: 
                        df = pd.read_json(sdk.run_query(query_id=tile.result_maker.query_id,result_format='json'))
                        pd.set_option("display.max_colwidth", 1000) #not the right place for this, but for some reason this is the only place i could get it to work without throwing error "NameError: name 'pd' is not defined"
                    except: 
                        failed_to_get_data = True
                    output = {'df':df,
                            "query_id":tile.result_maker.query_id,
                            "is_empty": df.empty,
                            "shape":df.shape,
                            "tile_title":tile.title, 
                            "could_get_api_data":failed_to_get_data}
                    
                    dfs.append(output)
                else: #handle case of a likely merge query
                    try: 
                        merge_list = sdk.merge_query(tile.merge_result_id)
                    except:
                        failed_to_get_data = True
                    for source_query in merge_list.source_queries:
                        try:
                            df = pd.read_json(sdk.run_query(query_id=source_query.query_id,result_format='json'))
                        except:
                            failed_to_get_data = True
                        output = {'df':df,
                            "query_id":source_query.query_id,
                            "is_empty": df.empty,
                            "shape":df.shape,
                            "tile_title":tile.title, 
                            "could_get_api_data":failed_to_get_data}
                        dfs.append(output)
        return dfs