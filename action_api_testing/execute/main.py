import functions_framework
import base64
import zipfile 
import os
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
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

    with pd.ExcelWriter(f'/tmp/{file_name}') as writer:  
        for file in zf.namelist():
            df = pd.read_csv(zf.open(file))  
            sheet_name = file.split("/")[1].split(".")[0] # Example of file:  'dashboard-zocdoc_jhu_covid/filters_applied.csv'
            print(sheet_name)
            df.to_excel(writer, sheet_name=sheet_name,index=False)

    message = Mail( from_email=email,
                    to_emails=email,
                    subject='Testing Sending Email from Action Hub',
                    html_content='<strong>Fingers Crossed!</strong>')
    
    with open(f'/tmp/{file_name}', 'rb') as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(file_name),
        FileType('application/xls'),
        Disposition('attachment')
    )
    message.attachment = attachedFile
    try:
        print('SENDGRID auth',os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return f"{response.__dict__}"