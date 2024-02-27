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

from looker_sdk import init40 
from urllib3 import disable_warnings,exceptions 
from _lco.colorprint import ColorPrint

disable_warnings(exceptions.InsecureRequestWarning) # Disabling https warning (self-signed warning), remove when accessing your own endpoint

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
        self.sdk = init40(self.config_file, section =self.config_instance)
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
        # print(f"\033[93mSwitched to {self.environment} environment\033[00m")
    
    def checkout_dev_branch(self,project_name:str,branch_name:str) -> None:
        """
        overview: 
         - Updates API to call data from a specific branch
        args:
         - project_name: Looker project name
         - branch_name: Name of branch being developed on, note please commit all code prior to running this method
        """
        # Step 1: Swap to Dev Mode
        self.switch_environment()
        # print("Note: Please ensure dev branch has all code committed prior to running.")
        body = {"name":branch_name}
        self.sdk.update_git_branch(project_id=project_name, body=body)
        print(f"Note: Dev instance set to {branch_name} in {project_name}")
    
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
        me = self.sdk.me()
        return f"API Connection to {self.config_instance} with User:{me.display_name}-Email:{me.email} API Credentials was successful."