import functions_framework
from icon import icon_data_uri

@functions_framework.http
def action_list(request):
    payload = request.get_json()
    print("list_actions received request:", payload)  
    actions_list = {
      "integrations": [
        {
          "name": "test_excel",
          "label": "Email Combined CSV as Single Excel File",
          "description": "Combines a Looker dashboards tiles into a single Excel, each sheet maps to one tile.",
          "form_url": "https://us-central1-ryancustomerhosted.cloudfunctions.net/forms" ,
          "url": "https://us-central1-ryancustomerhosted.cloudfunctions.net/post_execution",
          "supported_action_types": ["dashboard"],
          "supported_formats": ["csv_zip"],
          "icon_data_uri": icon_data_uri,
          "supported_download_settings": ["push"]
        }]}
    return actions_list