import functions_framework
import base64
import zipfile 
import os
import pandas as pd
import yagmail
from google.cloud import storage
import io

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

    data = request['attachment']['data']
    decoded_file = base64.b64decode(data)
    zf = zipfile.ZipFile(io.BytesIO(decoded_file), "r")
    print("List of files from dashboard:",zf.namelist())

    # Retrieve the 
    storage_client = storage.Client()
    bucket = storage_client.bucket("lookeraction_cloudfunction")
    for blob in bucket.list_blobs():
        print("Name of blob in gcp bucket:",blob.name)

    with pd.ExcelWriter(f'/tmp/{file_name}') as writer:  
        for file in zf.namelist():
            df = pd.read_csv(zf.open(file))  
            sheet_name = file.split("/")[1].split(".")[0] # Example of file:  'dashboard-zocdoc_jhu_covid/filters_applied.csv'
            print(sheet_name)
            df.to_excel(writer, sheet_name=sheet_name,index=False)

    try:
        user_email = os.environ.get('user_email')
        password = os.environ.get('gmail_password')
        yag = yagmail.SMTP(user=user_email,
                        password=password)
        contents = [
            "Please Find Single Excel File Excel Report which Combines a CSV Zip File"
        ]
        yag.send(email, 'Looker Action API Triggered Email', contents, attachments=f'/tmp/{file_name}')
    except:
        print("Error Sending Email")

    return f"{request.__dict__}"