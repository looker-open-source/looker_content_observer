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

from pandas import read_json, DataFrame
from _lco.colorprint import ColorPrint
import logging
from json import JSONDecodeError
from looker_sdk import init40,rtl,error

class Look: 
    def __init__(self,look_id:str) -> None:
        self.look_id = look_id
        self.look_data_error = False
        self.looker_error_sdk_message = None

    def get_look(self, sdk:init40) -> list:
        return sdk.look(self.look_id)
    
    def get_look_data(self,get_look_api_call:object,sdk:init40):
        logging.info(ColorPrint.yellow + "Retrieving Data for Look" + ColorPrint.end)
        name_of_look = get_look_api_call.title
        if name_of_look == None or name_of_look == '':
            name_of_look = "None"
            logging.info(ColorPrint.yellow + f"Could not find a title/name for look_id of:{self.look_id}" + ColorPrint.end)
        if get_look_api_call.query.id is not None:                
            try:
                df = read_json(sdk.run_query(query_id=get_look_api_call.query.id,
                                         result_format='json',
                                         )
                                    )
                assert "looker_error" not in df.columns.values.astype(str)
                return df.astype(str)
            except AssertionError:
                error_message = "Error in API call, Error in SQL, Looker could not Compile SQL"
                logging.warning(ColorPrint.red + f"{error_message}.\n:" + ColorPrint.end)
                logging.warning(ColorPrint.red + f"Looker SDK Error in SQL for {self.look_id}" + ColorPrint.end)
                self.look_data_error = True
                self.looker_error_sdk_message = df.values[0][0]
            except (JSONDecodeError,rtl.serialize.DeserializeError,error.SDKError):                
                error_message = "Error in API call, Empty JSON returned due to HTTPS Timeout Error from tile query type"
                logging.warning(ColorPrint.red + f"{error_message}" + ColorPrint.end)
                self.look_data_error = True
                self.looker_error_sdk_message = error_message            
            except:
                error_message = "General Error: Could not retrive the data from Look"
                self.look_data_error = True
                self.looker_error_sdk_message = error_message
                logging.warning(ColorPrint.red + f"Could not retrieve data for :{self.look_id}" + ColorPrint.end)
        
        logging.warning(ColorPrint.red + f"Could not retrieve data, returning None for Look {self.look_id}" + ColorPrint.end)
        return None