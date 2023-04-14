import pandas as pd
class Dashboard: 
    def __init__(self,dashboard_id) -> None:
        self.dashboard_id = dashboard_id

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
        tiles_in_dashboard = self.get_all_dashboard_elements(sdk)
        dfs = []
        for tile in tiles_in_dashboard:
            try:
                df = pd.read_json(sdk.run_inline_query(result_format='json',body = tile.query))
                # Apply a sorting to all columns, columns sorted in ascending order
                dfs.append(self.sort_all_columns(df))
            except: 
                print("Error with tile element of type:",self.map_tile_metadata_to_type(tile))
        return dfs
    
    def map_tile_metadata_to_type(self,tile):
        if tile.title:
            if tile.query:
                return "Tile"
            else: 
                return "Tile:Merged Query"

        if tile.rich_content_json:
            return "TextBox or Button/Link"

        if tile.title_text_as_html:
            return "Markdown File"
