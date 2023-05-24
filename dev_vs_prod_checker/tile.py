import pandas as pd
from colorprint import ColorPrint
import json
import logging
# TODO - Create mapping of tiles that captures each type of tile
# TODO - Return within tile.py class methods to retrieve the data per tile based on the correct tile type
class Tile: 
    def __init__(self,tile, dashboard_layout:list[object]) -> None:
        self.tile = tile
        self.dashboard_layout = dashboard_layout 
        self.tile_name = self.get_name_of_tile() # Returns name of tile
        self.tile_type = self.get_type_of_tile() # Returns type of tile, i.e. viz or button or text
        self.tile_id = self.get_tile_id() # Returns the dashboard id of the tile
        self.tile_layout = "-".join(map(str,self.get_tile_position()))
        self.tile_pkey = f"{self.tile_layout}|{self.tile_name}|{self.tile_type}"

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
        # TODO: Add unit test, filter element should always resolve to length of 1
        layouts = self.dashboard_layout
        logging.debug(ColorPrint.blue + f"# of elemements in tiles:{len(layouts)}" + ColorPrint.end)
        logging.debug(ColorPrint.blue + f"Keys within layout are:{layouts[0].__dict__.keys()}" + ColorPrint.end)
        filter_for_tile = list(filter(lambda layouts : layouts['id'] == self.get_tile_id(),layouts[0].dashboard_layout_components ))        
        logging.debug(ColorPrint.blue + f"Filtered tile:{filter_for_tile}" + ColorPrint.end)
        layout = (filter_for_tile[0].row,
                                    filter_for_tile[0].column,
                                    filter_for_tile[0].width,
                                    filter_for_tile[0].height)
        
        return layout