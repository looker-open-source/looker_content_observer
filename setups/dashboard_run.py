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

from _lco.dashboardchecker import DashboardChecker
import logging 
from _lco.test import TestResult
from _lco.colorprint import ColorPrint
from pandas import concat



def run_dashboard_tests(dashboards_to_check:list,
                        instances:list,
                        tests_to_run:dict) -> tuple:
    """
    - Retrieves data for each test 
    :returns: each dashboard as element within list, all dashboards combined into a single pandas dataframe 
    """
    dash_data = []
    assert tests_to_run.get('dashboard_tests') is not None, f"No key found for dashboard tests, please confirm the config_tests.yaml file is being passed in"

    for dashboard_id in dashboards_to_check:
        dc = DashboardChecker(dashboard_id,
                              instances,
                              tests_to_run['dashboard_tests'])
        data = dc.get_data_for_test()
        logging.info(ColorPrint.yellow + f"Retrieved data for dash:{dashboard_id} of shape:{data.shape}" + ColorPrint.end)
        logging.info(ColorPrint.yellow + f"Applying pandas tests to data" + ColorPrint.end)
        # Apply test of equality
        data['is_data_equal'] = TestResult.is_data_equal(data)
        dash_data.append(data)
    # Combine all dataframes together
    return dash_data, concat([*dash_data], ignore_index=True)