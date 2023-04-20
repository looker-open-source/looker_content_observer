import pandas as pd
import looker_sdk
import urllib3
import time
import configparser
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disabling https warning (self-signed warning), remove when accessing your own endpoint

"""
Note: 
- Script will need a looker.ini file in order to run
- See: https://developers.looker.com/api/getting-started 
"""


class LookerEnvironment:
    """
    overview: 
    - 

    init: 
    - See init args for sdk: https://github.com/looker-open-source/sdk-codegen/blob/main/python/looker_sdk/__init__.py#L71 
    """
    def __init__(self, environment:str, config_file:str=None, config_instance:str = None) -> None:
        self.config_file = "looker.ini" if config_file is None else config_file
        self.config_instance = 'Looker' if config_instance is None else config_instance 
        self.sdk = looker_sdk.init40(self.config_file, section =self.config_instance)
        self.me = self.sdk.me()
        self.environment = environment

    def switch_environment(self) -> None:
        """
        overview: 
         - Switches either to production or development environment
        args:
         - environment:str -> Values are either: 'production' or 'dev'
        :returns: 
         - session object -> Use to confirm the session.workspace_id == desired_environment, i.e production or dev  
        """
        body = {"workspace_id":self.environment}
        self.sdk.update_session(body=body)
        print(f"\033[93mSwitched to {self.environment} environment\033[00m")
    
    def checkout_dev_branch(self,project_name:str,branch_name:str) -> None:
        """
        overview: 
         - Updates API to call data from a specific branch
        args:
         - project_name: Looker project name
         - project_name: Name of branch being developed on, note please commit all code prior to running this method
        """
        print("Note: Please ensure dev branch has all code committed prior to running.")
        body = {"name":branch_name}
        self.sdk.update_git_branch(project_id=project_name, body=body)
        print(f"Switched to {branch_name} in {project_name}")
    
    def get_session(self) -> object:
        """
        overview: 
         - Helper function to confirm if sdk is calling data from either production or development
        :returns:
         - Looker_SDK Session Object
         - Example: ApiSession(can={'view': True, 'update': True}, workspace_id='production', sudo_user_id=None)
        """
        return self.sdk.session()

    def __str__(self) -> str:
        """
        print sdk.me() to confirm if sdk is authenticated correctly
        """
        return f"{self.me.__dict__}"

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
        merge_list = []
        test2=[]
        for tile in tiles_in_dashboard:
            type_of_tile = self.map_tile_metadata_to_type(tile)
            #print(type_of_tile)
            if type_of_tile == 'Tile':
                df = pd.read_json(sdk.run_inline_query(result_format='json',body = tile.query))
                # Apply a sorting to all columns, columns sorted in ascending order
                dfs.append(self.sort_all_columns(df))
            elif type_of_tile == 'Tile:Merged Query':
                merge_list = sdk.merge_query(tile.merge_result_id)
                #query_id_list = []
                for source_query in merge_list.source_queries:
                    #query_id_list.append(source_query.query_id)
                    df = pd.read_json(sdk.run_query(query_id=source_query.query_id,result_format='json'))
                    dfs.append(self.sort_all_columns(df))
    #                 
    # Here's another method of appending to dfs but using run_inline_query
    # First define this above: 
    #   test2=[]
    # Then add this instead of the current for loop on source_query:
    #             for source_query in merge_list.source_queries:
    #                  test2.append(sdk.query(query_id=source_query.query_id,fields="model,view,fields,pivots,fill_fields,filters,filter_expression,sorts,limit,column_limit,total,row_total,subtotals,vis_config,filter_config,visible_ui_sections,dynamic_fields,query_timezone"))
    #             for querydef in test2:
    #                 df = pd.read_json(sdk.run_inline_query(result_format='json',body = querydef))
    #                 dfs.append(self.sort_all_columns(df))           
                
                
                
                    # print(sdk.run_inline_query(result_format='json',body = querydef))
                #print(query_id_list)
                #print(test2)

                # for query_id in query_id_list:
                #     test2=sdk.query(query_id)

                
                # df = pd.read_json(sdk.run_query(query_id=test2result_format='json',body = test2.Query))
                # print(test.source_queries['query_id'])
                # for i in df.source_queries:
                #     print(test.source_queries[i]['query_id'])
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

if __name__ == '__main__':
    # Set the branch and project
    config = configparser.ConfigParser()
    
    # Turn into argparse
    config_file = "looker.ini"
    config.read(config_file)
    dev_branch = config['gcpm234']['dev_branch']
    project_name = config['gcpm234']['project']
    

    # Instantiate the dev and prod sdks
    prod = LookerEnvironment('production',config_instance='gcpm234')
    dev = LookerEnvironment('dev',config_instance='gcpm234')
    # print(dev.me)
    #Change/Enter the dashboard id in the below: 
    # Example: https://my.looker.com19999/dashboards/4 -> Dashboard('4')
    dashboard = Dashboard('13') # Enter the dashboard number you'd like to test here

    print("\033[95mTesting Production:\033[00m")
    print("Looping through all dev tiles for the dashboard:")
    prod_tiles = dashboard.get_all_tiles_data(prod.sdk)
    for tile in prod_tiles:
        print(tile.head())
    
    print("\033[95mTesting Development:\033[00m")
    # Step 1: Call method to switch to development 
    dev.switch_environment()
    # [Optional]: Output session method to confirm switch was succesful
    print(dev.get_session())
    # Step 2: Swap to the dev branch you want to test
    dev.checkout_dev_branch(project_name,dev_branch)
    print("Looping through all dev tiles for the dashboard:")
    dev_tiles = dashboard.get_all_tiles_data(dev.sdk)
    print("Outputting the first 5 rows from each tile:")
    for tile in dev_tiles:
        print(tile.head())

    # for tile in prod_tiles:
    #     print(tile.head())
    #     print dev_tiles


