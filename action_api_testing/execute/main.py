import functions_framework
import base64
import zipfile 
import os
import pandas as pd
import yagmail
from google.cloud import storage
import io
import openpyxl

def load_excel_file(file_loc,list_of_vals, sheet_name):
    wb = openpyxl.load_workbook(file_loc)
    ws = wb[sheet_name]
    for row_data in list_of_vals:
        ws.append(row_data)
    wb.save(file_loc)

@functions_framework.http
def action_execute(request):
    """
    Combines zipped CSV file into singel Excel File, emails Excel File to receipient
    """
    request = request.get_json()
    print('Request Payload:', request)

    #  Retrieve Form Information: Email + File Name
    email = request['form_params']['email_address']
    file_name = request['form_params']['excel_file_name'] + ".xlsx"

    # Retrieve the zipped CSV data from the API 
    data = request['attachment']['data']
    decoded_file = base64.b64decode(data)
    zf = zipfile.ZipFile(io.BytesIO(decoded_file), "r")
    print("List of files from dashboard:",zf.namelist())

    # Retrieve the template from GCS Bucket
    storage_client = storage.Client()
    template_file_loc = f"/tmp/{file_name}.xlsx"
    bucket = storage_client.bucket("lookeraction_cloudfunction")
    blob = bucket.blob('excel_template_vo.xlsx') # You can make this dynamic similar to the email by modifying the Looker Action form
    buffer = io.BytesIO()
    blob.download_to_file(buffer)
    wb = openpyxl.load_workbook(buffer)
    wb.save(template_file_loc)    

    # Write each csv from the zip file into the template
    for file in zf.namelist():
        df = pd.read_csv(zf.open(file))  
        sheet_name = file.split("/")[1].split(".")[0] # Example of file:  'dashboard-zocdoc_jhu_covid/filters_applied.csv'
        list_of_vals = df.values.tolist()
        load_excel_file(template_file_loc,list_of_vals,sheet_name)

    # with pd.ExcelWriter(f'/tmp/{file_name}') as writer:  
    #     for file in zf.namelist():
    #         df = pd.read_csv(zf.open(file))  
    #         sheet_name = file.split("/")[1].split(".")[0] # Example of file:  'dashboard-zocdoc_jhu_covid/filters_applied.csv'
    #         print(sheet_name)
    #         df.to_excel(writer, sheet_name=sheet_name,index=False)

    try:
        user_email = os.environ.get('user_email')
        password = os.environ.get('gmail_password')
        yag = yagmail.SMTP(user=user_email,
                        password=password)
        contents = [
            "Please Find Single Excel File Excel Report which Combines a CSV Zip File"
        ]
        yag.send(email, 'Looker Action API Triggered Email', contents, attachments=template_file_loc)
        print("Email succesfully Sent")
    except:
        print("Error Sending Email")

    return f"{request}"