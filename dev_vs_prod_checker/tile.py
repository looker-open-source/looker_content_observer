import pandas as pd
from colorprint import ColorPrint
import json
import logging

class Tile: 
    def __init__(self,tile) -> None:
        self.tile = tile

    def get_name_of_tile(self):
        if self.tile.type == 'button':
            try:
                return json.loads(self.tile.rich_content_json)['text']
            except: 
                return "Error with parsing JSON of button"
        elif self.tile.type == 'text':
            return self.tile.title_text_as_html
        elif self.tile.type == 'vis':
            return self.tile.title
        else:
            return "Unmapped"