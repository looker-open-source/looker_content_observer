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
            print(dash_element)
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
            if tile.type == 'vis':
                if tile.query_id != None: 
                    df = pd.read_json(sdk.run_query(query_id=tile.query_id,result_format='json'))
                    print(df.head())
                    dfs.append(df)
                elif tile.merge_result_id != None:
                    merge_list = sdk.merge_query(tile.merge_result_id)
                    for source_query in merge_list.source_queries:
                        df = pd.read_json(sdk.run_query(query_id=source_query.query_id,result_format='json'))
                        dfs.append(df)
        return dfs