import pandas as pd
from _lco.colorprint import ColorPrint
from _lco.tile import Tile
import json
import looker_sdk

class Look: 
    def __init__(self,look_id:str) -> None:
        self.look_id = look_id

    def get_look(self, sdk:looker_sdk) -> list:
        return sdk.look(self.look_id)
    
    def get_look_data(self,sdk:looker_sdk,tile):
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
    