import pandas as pd
from colorprint import ColorPrint
import json
import logging
from lookerenvironment import LookerEnvironment

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
            return rename_if_title_none(self.tile.title_text_as_html)
        elif self.tile.type == 'vis':
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
            if self.tile.merge_result_id is not None: 
                return "Merged Query"
            elif self.tile.look_id != None and self.tile.result_maker.query_id is not None:
                return "Look"
            elif self.tile.look_id == None and self.tile.result_maker.query_id is not None:
                return "Tile"
            else:
                logging.warning(f"Unmapped vis type tile found:{self.tile}") 
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
        logging.debug(ColorPrint.blue + f"Keys within layout are:{layouts[0].__dict__.keys()}" + ColorPrint.end)
        filter_for_tile = list(filter(lambda layouts : layouts['id'] == self.get_tile_id(),layouts[0].dashboard_layout_components ))        
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
    
    def get_tile_data(self):
        # Get data for single tile viz
        if self.tile_type == "Tile":
            try:
                df = pd.read_json(self.sdk.run_query(query_id=self.tile.result_maker.query_id,result_format='json'))
                logging.info(ColorPrint.yellow + f"Tile had following data:{df.head()}" + ColorPrint.end)
                assert "looker_error" not in df.columns.values
                self.tile_df = df.astype(str)
                self.tile_df_dimensions = df.shape
            except AssertionError:
                logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for tile" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = df.values[0][0]
            except:
                logging.warning(ColorPrint.red + f"Error running query, could not retrieve data" + ColorPrint.end)
                self.tile_data_error = True
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
                    logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for tile" + ColorPrint.end)
                    self.tile_data_error = True
                    self.looker_error_sdk_message = df.values[0][0]
                except:
                    logging.warning(ColorPrint.red + f"Error running query, could not retrieve data" + ColorPrint.end)
                    self.tile_data_error = True
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
                logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for tile" + ColorPrint.end)
                self.tile_data_error = True
                self.looker_error_sdk_message = df.values[0][0]
            except:
                logging.error("Error running following tile:",self.tile_pkey)
                self.tile_data_error = True
        else:
            logging.info(ColorPrint.yellow + f"Tile: {self.tile_pkey} skipped as not of type 'vis'" + ColorPrint.end)




