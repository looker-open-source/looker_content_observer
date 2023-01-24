# Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose. Your use of it is subject to your agreement with Google. 
import json
import functions_framework

@functions_framework.http
def action_form(request):
    """
    Function defines the form users wil fill out
    Forms: 
    - Email Address
    - Excel File Name 
    """
    payload = request.get_json()
    print("Request Payload:", payload)
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