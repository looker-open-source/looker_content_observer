import json
@functions_framework.http
def action_form(request):
    payload = request.get_json()
    print("action_form received request:", payload)
    print("request data for form: ", request)
    form = [{"name": "Include Cover Page", 
            "label": "Include page with title, time of download, and filters", 
            "type":"select",
            "required": True, 
            "sensitive": False, 
            "options": [{"name": "include_yes","label": "Yes"},
                        {"name": "include_no", "label": "No"}]
            },
            { "name": "Email addresses",
            "type": "text",
            "required": True
            }
        ]
    return json.dumps(form)