# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from _lco.colorprint import ColorPrint
import json

class Dashboard: 
    def __init__(self,dashboard_id:str) -> None:
        self.dashboard_id = dashboard_id

    def get_dashboard(self, sdk:object) -> list:
        """
        :docs: https://developers.looker.com/api/explorer/4.0/methods/Dashboard/dashboard?sdk=py&s=dashboard
        :returns: API call from get dashboard endpoint
        """ 
        return sdk.dashboard(self.dashboard_id)

    def get_dashboard_layout(self,sdk:object) -> list: 
        """
        :docs: https://developers.looker.com/api/explorer/4.0/methods/Dashboard/dashboard_dashboard_layouts?sdk=py&s=dashboard_dashboard_layouts
        :returns: API call from get dashboard layout endpoint
        """ 
        return sdk.dashboard_dashboard_layouts(self.dashboard_id)

    def get_all_dashboard_elements(self, sdk:object) -> list:
        """
        :docs: https://developers.looker.com/api/explorer/4.0/methods/Dashboard/dashboard_dashboard_elements?sdk=py&s=elements 
        :returns: All tile infromation from a dashboard (based on the dashboard id)
        """ 
        return sdk.dashboard_dashboard_elements(self.dashboard_id)

    def sort_all_columns(self,df) -> pd.DataFrame:
        """
        - Helper function to help ensure the dataframe is sorted in the same order
        :returns: Sorted dataframe in ascending order
        """
        return df.sort_values(by=df.columns.tolist())
    
    def get_all_tiles_data(self,sdk:object) -> list:
        """
        - Retrieves the underlying data for a tile, all tiles are turned into separate dataframes and appended to a list 
        - :returns: list of dataframes
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
    #TODO This appears to be unused code... instead using get_name_of_tile() in tile.py - confirm can delete?
    def get_name_of_tile(self,tile):
        if tile.type == 'button':
            try:
                return json.loads(tile.rich_content_json)['text']
            except: 
                return "Error with parsing JSON of button"
        elif tile.type == 'text':
            return tile.title_text_as_html
        elif tile.type == 'vis':
            # Look tiles store title differently from merge tiles and regular tiles
            if tile.look_id != None and tile.result_maker.get('query_id') is not None:
                return tile.look.title
            else:
                return tile.title
        else:
            return "Unmapped"

