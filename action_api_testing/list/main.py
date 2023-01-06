import functions_framework
from icon import icon_data_uri

@functions_framework.http
def action_list(request):
    payload = request.get_json()
    print("list_actions received request:", payload)  
    actions_list = {
      "integrations": [
        {
          "name": "test_excel_2",
          "label": "Test 2 as Folders",
          "description": "Download a dashboard as a tabbed Excel file",
          "form_url": "https://us-central1-ryancustomerhosted.cloudfunctions.net/test2/action_form" ,
          "url": "https://us-central1-ryancustomerhosted.cloudfunctions.net/test2/action_execute",
          "supported_action_types": ["dashboard"],
          "supported_formats": ["csv_zip"],
          "icon_data_uri": icon_data_uri,
          "supported_download_settings": ["push"]
        }]}
    return actions_list