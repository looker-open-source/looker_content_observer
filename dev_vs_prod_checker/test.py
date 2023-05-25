import pandas as pd
from dashboard import Dashboard
from tile import Tile
import logging
from colorprint import ColorPrint
import json

class TestResult:
 
    def is_dataframe_equal(a:pd.DataFrame,b:pd.DataFrame) -> bool:
        return a.equals(b)
    
    def is_data_equal(df:pd.DataFrame) -> bool:
        """
        - Find where the column == 'test', all columns to the right of this will be the ones we want to test 
        """
        test_index = (df.columns.get_loc("test") + 1)
        try:
            assert (df.shape[1] - test_index) > 1, f"Test only as one row"
            return list(map(lambda values: len(set([tuple(val) if type(val)==list else val for val in values])) ==1  , df.iloc[:,test_index:].values))
        except AssertionError:
            return ['N/A'] * df.shape[0]      

class Test:    
    def get_number_tiles_in_dash(dash:Dashboard):
        return len(dash.dashboard_elements)
    
    def get_number_filters_in_dash(dash:Dashboard):
        return len(dash.dashboard_filters)
    
    def get_hash_of_all_filters(dash:Dashboard):
        """
        overview: 
        - Each dashboard element is an object, this method converts the object into a string and then hashes the string and is used in a check to compare hashes
        - Note: This method will likely fail if the id of the dashboard element has changed
        :returns: 
        - Hash of representing all dashboard elemtns
        """
        return hash(frozenset([str(val) for val in sorted(dash.dashboard_filters, key= lambda obj: obj.id)]))

    def get_type_of_dashboard(dash:Dashboard):
        # UDD - User defined dashboard
        return 'LookML Dashboard' if dash.lookml_link_id else 'UDD'
    
    def get_hash_of_query_from_dashboard(dash):
        queries = []
        for dash_element in dash.dashboard_elements:
            pass
            # print(dash_element)
        return None
    
    def get_composition_of_dashboard(dash:Dashboard):
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
    
    # TODO: Debug this
    def get_tile_names(dash:Dashboard):
        composition = {}
        for tile in dash.dashboard_elements:
            t = Tile(tile,dash)
            logging.debug(ColorPrint.blue + f"Checking tile:{t.tile_name}" + ColorPrint.end)
            if t.tile_name not in composition:
                composition[t.tile_name] = 1
            else:
                composition[t.tile_name] += 1
        # Sort by keys
        return sorted(composition.items())

    def get_tile_data(tile:Tile):
        if tile.tile_type == "Merged Query":
            return tile.tile_merged_dfs
        else:
            return tile.tile_df

    def get_tile_dimensions(tile:Tile):
        if tile.tile_type == "Merged Query":
            return tile.tile_merged_dfs_dimensions
        else:
            return tile.tile_df_dimensions

    def get_tile_position(tile:Tile):
        return tile.tile_layout

    def get_api_success(tile:Tile):
        if tile.tile_data_error:
            return False
        else:
            return True