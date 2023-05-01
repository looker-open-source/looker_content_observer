import pandas as pd
from colorprint import ColorPrint
import json

class Dashboard: 
    def __init__(self,dashboard_id) -> None:
        self.dashboard_id = dashboard_id

    def get_dashboard(self, sdk:object) -> list:
        """
        """ 
        return sdk.dashboard(self.dashboard_id)

    def get_all_dashboard_elements(self, sdk:object) -> list:
        """
        :returns: All tile infromation from a dashboard (based on the dashboard id)
        - Example: https://my.looker.com19999/dashboards/4 -> dashboard_id = '4'
        """ 
        return sdk.dashboard_dashboard_elements(self.dashboard_id)

    def sort_all_columns(self,df) -> pd.DataFrame:
        """
        overview:
        - Helper function to help ensure the dataframe is sorted in the same order
        :returns:
        - Asc. Sorted dataframe
        """
        return df.sort_values(by=df.columns.tolist())
    
    def get_all_tiles_data(self,sdk:object) -> list:
        """
        overview:
        - Retrieves the underlying data for a tile, all tiles are turned into separate dataframes and appended to a list 
        :returns:
        - list of dataframes
        """
        try:
            tiles_in_dashboard = self.get_all_dashboard_elements(sdk)
        except:
            print("Error when attempting get_all_dashboard_elements() method. Unable to retrieve dashboard elements")
        
        if len(tiles_in_dashboard) == 0:
            raise Exception(ColorPrint.red + "The dashboard appears to have no elements in it." + ColorPrint.end)
        
        dfs = []
        merge_list = []
        for tile in tiles_in_dashboard:
            type_of_tile = self.map_tile_metadata_to_type(tile)
            if type_of_tile == 'Tile':
                df = self.map_tile(sdk,tile)
                # dfs.append(self.sort_all_columns(df))
                dfs.append(df)
            elif type_of_tile == 'Tile:Merged Query':
                merge_list = sdk.merge_query(tile.merge_result_id)
                #query_id_list = []
                for source_query in merge_list.source_queries:
                    #query_id_list.append(source_query.query_id)
                    df = pd.read_json(sdk.run_query(query_id=source_query.query_id,result_format='json'))
                    dfs.append(self.sort_all_columns(df))
            else:
                print(f"Skipping: {type_of_tile}")
        return dfs
    
    def map_tile_metadata_to_type(self,tile):
        if tile.title:
            #print(tile.merge_result_id)
            if tile.merge_result_id:
                return "Tile:Merged Query"
            else: 
                return "Tile"

        if tile.rich_content_json:
            return "TextBox or Button/Link"

        if tile.title_text_as_html:
            return "Markdown File"
        
    def map_tile(self,sdk:object,tile):
        """
        overview: 
        - Depending on if the tile is from a LookML dashboard or UDF, the parameters and methods to retrieve the data from the dashboard are differnet
        """
        if tile.result_maker:
            if tile.result_maker.query_id:
                # return pd.read_json(sdk.run_inline_query(result_format='json',body = tile.result_maker.query))
                return pd.read_json(sdk.run_query(result_format='json',query_id=tile.result_maker.query_id))
            else:
                print(ColorPrint.red + "Else hit" + ColorPrint.end)
                print(tile.result_maker.query_id)
        else: 
            pass
    
    def get_name_of_tile(self,tile):
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

    