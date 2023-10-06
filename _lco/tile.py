#License Header

import pandas as pd
from _lco.colorprint import ColorPrint
from _lco.lookerenvironment import LookerEnvironment
import json
import logging
import looker_sdk

class Tile: 
    def __init__(self,tile, dashboard_layout:list, sdk:LookerEnvironment) -> None:
        self.tile = tile
        self.dashboard_layout = dashboard_layout 
        self.sdk = sdk
        self.tile_name = self.get_name_of_tile() # Returns name of tile
        self.tile_type = self.get_type_of_tile() # Returns type of tile, i.e. viz or button or text
        self.tile_id = self.get_tile_id() # Returns the dashboard id of the tile
        self.tile_layout = "-".join(map(str,self.get_tile_position()))
        self.tile_pkey = f"{self.tile_layout}|{self.tile_name}|{self.tile_type}"
        self.tile_df = None
        self.tile_df_dimensions = None
        self.tile_merged_dfs = []
        self.tile_merged_dfs_dimensions = []
        self.tile_data_error = False
        self.looker_error_sdk_message = None

    def get_name_of_tile(self):
        """
        :returns: Name of tile, usually derived from the tile's Title
        """
        rename_if_title_none = lambda val: "Untitled" if val == None or val == "" else val
        if self.tile.type == 'button':
            try:
                json_text = json.loads(self.tile.rich_content_json)['text']
                logging.debug(ColorPrint.blue + f"Text from JSON:{json_text}" + ColorPrint.end)
                return rename_if_title_none(json_text)
            except: 
                return "Error with parsing JSON of button"
        elif self.tile.type == 'text':
            # Two types of text tiles - markdown and "text"
            # TODO still need to do a better job extracting the h1 text from the text tile
            # Example: [{""type"":""h1"",""children"":[{""text"":""Awesome Title""}],""align"":""center""},{""type"":""p"",""children"":[{""text"":""Very awesome text""}]
            if self.tile.rich_content_json is None:
                return rename_if_title_none(self.tile.title_text_as_html)
            else: 
                return rename_if_title_none(self.tile.body_text)
        elif self.tile.type == 'vis':
            # Look tiles store title differently from merge tiles and regular tiles
            if self.tile.look_id != None and self.tile.result_maker.get('query_id') is not None:
                return rename_if_title_none(self.tile.look.title)
            else:
                return rename_if_title_none(self.tile.title)
        else:
            logging.debug(ColorPrint.blue + f"Unampped tile:{self.tile}" + ColorPrint.end)
            return "Unmapped"
        
    def get_type_of_tile(self) -> str:
        """
        :returns: Type of Tile ∈ {Merged Query,Look,Tile,Text,Button,Unmapped}
        """
        logging.debug(ColorPrint.blue + f"Checking tile of type:{self.tile.type}" + ColorPrint.end)
        if self.tile.type == 'vis': 
            try:
                if self.tile.merge_result_id is not None: 
                    return "Merged Query"
                # In certain cases, the result_maker will either be None (empty) or contain a query_id
                elif self.tile.look_id != None and self.tile.result_maker.get('query_id') is not None:
                    return "Look"
                elif self.tile.look_id == None and self.tile.result_maker.__dict__.get('query_id') is not None:
                    return "Tile"
                else:
                    error_message = "An unknown/unmapped visualization type was encountered, skipping evaluation for Tile."
                    logging.warning(f"Unmapped vis type tile found:{self.tile}") 
                    return "Unmapped Vis Tile"
            except AttributeError:
                error_message = "A Query_ID was found to be None, preventing methods used to classify / identify the type of tile"
                logging.warning(ColorPrint.red + f"{error_message}.\n:" + ColorPrint.end)
                logging.debug(self.tile) 
                logging.warning(ColorPrint.red + f"Note: Tile will be skipped" + ColorPrint.end)
                return "Unmapped Vis Tile"

        elif self.tile.type == 'text':
            return self.tile.type.capitalize()
        elif self.tile.type == 'button':
            return self.tile.type.capitalize()
        else: 
            return "Unmapped Tile Type"
    
    def get_tile_id(self):
        return self.tile.id
    
    def get_tile_position(self):
        """
        :returns: row, column, width, height coordinates for the tile's position within the dashboard
        """
        layouts = self.dashboard_layout
        logging.debug(ColorPrint.blue + f"Number of dictionaries returned by sdk.dashboard_dashboard_layouts: {len(layouts)}" + ColorPrint.end)
        dashboard_type = list(filter(lambda layouts : layouts['type'] != "drag",layouts ))        
        logging.debug(ColorPrint.blue + f"Dashboard is of type:{dashboard_type[0].type}" + ColorPrint.end)
        logging.debug(ColorPrint.blue + f"Length of dashboard_type:{len(dashboard_type)}" + ColorPrint.end)
        assert len(dashboard_type) == 1, f"Dashboard has more than 1 type within it" 

        logging.debug(ColorPrint.blue + f"Tile ID:{self.get_tile_id()}" + ColorPrint.end)
        filter_for_tile = list(filter(lambda dash_id : dash_id['dashboard_element_id'] == self.get_tile_id(),dashboard_type[0].dashboard_layout_components ))        
        logging.debug(ColorPrint.blue + f"Filtered tile:{filter_for_tile}" + ColorPrint.end)

        # Raise an error in the cases that filter expresison finds more than 1 dashboard with same element_id
        assert len(filter_for_tile) == 1, f"More than 1 tile within dashboard with the same tile_id OR tile_id not found" 

        # Layout represents the dimensions of: row, column, width, heigh 
        # -> Example (0,4,4,2): tile starts on the first row, end on column 4, is 4 columns wide, and has height of 2 rows 
        layout = (filter_for_tile[0].row,
                                    filter_for_tile[0].column,
                                    filter_for_tile[0].width,
                                    filter_for_tile[0].height)
        return layout
    
    # TODO: Break this up into something my DRY
    def get_tile_data(self):
        # Get data for single tile viz
        if self.tile_type == "Tile":
            try:
                logging.debug(ColorPrint.blue + f"Executing sdk.run_query for tile:{self.tile_name}" + ColorPrint.end)
                df = pd.read_json(self.sdk.run_query(query_id=self.tile.result_maker.query_id,result_format='json'))
                logging.info(ColorPrint.yellow + f"Tile had following data:{df.head()}" + ColorPrint.end)
                assert "looker_error" not in df.columns.values.astype(str)
                self.tile_df = df.astype(str)
                self.tile_df_dimensions = df.shape
            except AssertionError:
                error_message = "Error in API call, Error in SQL, Looker could not Compile SQL"
                logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for {self.tile_name}" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = df.values[0][0]
            except (json.JSONDecodeError,looker_sdk.rtl.serialize.DeserializeError,looker_sdk.error.SDKError):                
                error_message = "Error in API call, Empty JSON returned due to HTTPS Timeout Error from tile query type"
                logging.warning(ColorPrint.red + f"{error_message}" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = error_message            
            except:
                logging.warning(ColorPrint.red + f"General Error running query, could not retrieve data" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = "General Error in API call, could not retrieve data"
        # Get data for merged query tile viz
        elif self.tile_type == "Merged Query":
            merge_list = self.sdk.merge_query(self.tile.merge_result_id)
            for source_query in merge_list.source_queries:
                try: 
                    df = pd.read_json(self.sdk.run_query(query_id=source_query.query_id,result_format='json'))
                    logging.info(ColorPrint.yellow + f"Tile had following data:{df.head()}" + ColorPrint.end)
                    logging.info(ColorPrint.yellow + f"Tile had following shape:{df.shape}" + ColorPrint.end)
                    assert "looker_error" not in df.columns.values
                    self.tile_merged_dfs.append(df.astype(str))
                    self.tile_merged_dfs_dimensions.append(df.shape)
                except AssertionError:
                    logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for tile from merged query" + ColorPrint.end)
                    self.tile_data_error = True
                    self.looker_error_sdk_message = df.values[0][0]
                except (json.JSONDecodeError,looker_sdk.rtl.serialize.DeserializeError,looker_sdk.error.SDKError):
                    error_message = "Error in API call, Empty JSON returned due to HTTPS Timeout Error from merged query"
                    logging.warning(ColorPrint.red + f"{error_message}" + ColorPrint.end)
                    self.tile_data_error = True
                    self.looker_error_sdk_message = error_message            
                except:
                    logging.warning(ColorPrint.red + f"General Error running query, could not retrieve data" + ColorPrint.end)
                    self.tile_data_error = True
                    self.looker_error_sdk_message = "General Error in API call, could not retrieve data"
        elif self.tile_type == "Look":     
            try:
                df = pd.read_json(self.sdk.run_query(query_id=self.tile.look.query.id,result_format='json'))
                logging.info(ColorPrint.yellow + f"Tile had following data:{df.head()}" + ColorPrint.end)
                logging.info(ColorPrint.yellow + f"Tile had following shape:{df.shape}" + ColorPrint.end)
                assert "looker_error" not in df.columns.values
                self.tile_df = df.astype(str)
                self.tile_data_dimensions = df.shape # Set the dimensions of the tile based on the underlying data
                logging.info(ColorPrint.yellow + f"Tile had following shape:{df.shape}" + ColorPrint.end)
            except AssertionError:
                logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for tile from Look" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = df.values[0][0]
            except (json.JSONDecodeError,looker_sdk.rtl.serialize.DeserializeError,looker_sdk.error.SDKError):
                error_message = "Error in API call, Empty JSON returned due to HTTPS Timeout Error from Look"
                logging.warning(ColorPrint.red + f"{error_message}" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = error_message            
            except:
                logging.warning("General Error attempting to retrieve Look's Data:",self.tile_pkey)
                self.tile_data_error = True
                self.looker_error_sdk_message = "General Error in API call, could not retrieve data"
        elif self.tile_type == 'Unmapped Vis Tile':
            error_message = "Unmapped Vis Tile: Underlying Data for Model/Look/Tile likely Missing"
            logging.warning(ColorPrint.red + error_message + ColorPrint.end)
            self.tile_data_error = True
            self.looker_error_sdk_message = error_message            
        else:
            logging.info(ColorPrint.yellow + f"Tile: {self.tile_pkey} skipped as not of type 'vis'" + ColorPrint.end)




