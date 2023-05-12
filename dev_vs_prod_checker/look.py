import pandas as pd
from colorprint import ColorPrint
import json

class Look: 
    def __init__(self,look_id,kwargs) -> None:
        self.look_id = look_id
        self.kwargs = kwargs

    def get_look(self, sdk:object) -> list:
        """
        """ 
        return sdk.look(self.look_id)

    def sort_all_columns(self,df) -> pd.DataFrame:
        """
        overview:
        - Helper function to help ensure the dataframe is sorted in the same order
        :returns:
        - Asc. Sorted dataframe
        """
        return df.sort_values(by=df.columns.tolist())
    
    def get_look_data(self,sdk:object) -> list:
        """
        overview:
        - Retrieves the underlying data for a look and puts that into a list of one element (to be compatible with dashboard testing)
        :returns:
        - list of dataframes
        """
        
        df = self.map_tile(sdk,tile)
        # dfs.append(self.sort_all_columns(df))
        return df
        
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

    