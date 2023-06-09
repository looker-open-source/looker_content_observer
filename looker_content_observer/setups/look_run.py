from _lco.lookchecker import LookChecker
import logging 
from _lco.test import TestResult
from _lco.colorprint import ColorPrint
from pandas import concat


def run_look_tests(look_to_check:list,
                        instances:list,
                        tests_to_run:dict) -> tuple:
    """
    - Retrieves data for each test 
    :returns: each dashboard as element within list, all dashboards combined into a single pandas dataframe 
    """
    dash_data = []
    assert tests_to_run.get('look_tests') is not None, f"No key found for dashboard tests, please confirm the config_tests.yaml file is being passed in"

    for look_id in look_to_check:
        lc = LookChecker(look_id,
                        instances,
                        tests_to_run['look_tests'])
        data = lc.get_data_for_test()
        logging.info(ColorPrint.yellow + f"Retrieved data for dash:{look_id} of shape:{data.shape}" + ColorPrint.end)
        logging.info(ColorPrint.yellow + f"Applying pandas tests to data" + ColorPrint.end)
        # Apply test of equality
        data['is_data_equal'] = TestResult.is_data_equal(data)
        dash_data.append(data)
    
    return dash_data, concat([*dash_data], ignore_index=True)