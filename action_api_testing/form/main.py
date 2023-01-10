import json
import functions_framework

@functions_framework.http
def action_form(request):
    payload = request.get_json()
    print("action_form received request:", payload)
    print("request data for form: ", request)
    form = [{ "name": "email_address",
              "label": "Email Address", 
                "type": "text",
                "required": True
            },
            { "name": "excel_file_name",
              "label": "Name of Excel File", 
                "type": "text",
                "required": True
            }
        ]
    return json.dumps(form)