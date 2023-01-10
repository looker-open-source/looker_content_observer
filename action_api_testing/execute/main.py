import functions_framework
import base64
import zipfile 
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

@functions_framework.http
def action_execute(request):
    request = request.get_json()
    print(' :', request)

    title = request['scheduled_plan']['title']
    title = title.replace(" ", "_").lower()

    email = request['form_params']['Email addresses']
    print("Email receipient", email)

    data = request['attachment']['data']
    decoded_file = base64.b64decode(data)
    zf = zipfile.ZipFile(decoded_file) 

    with pd.ExcelWriter('test_output.xlsx') as writer:  
        for file in zf.namelist():
            df = pd.read_csv(zf.open(file))
            sheet_name = file.split("/")[1].split(".")[0] # Example of file:  'dashboard-zocdoc_jhu_covid/filters_applied.csv'
            print(sheet_name)
            df.to_excel(writer, sheet_name=sheet_name,index=False)

    message = Mail(
                    from_email=email,
                    to_emails=email,
                    subject='Testing Sending Email from Action Hub',
                    html_content='<strong>Fingers Crossed!</strong>')
    encoded_file = base64.b64encode(writer).decode()
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('test_output.xlsx'),
        FileType('application/xls'),
        Disposition('attachment')
    )
    message.attachment = attachedFile
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return f"{response.__dict__}"


    return f"{request}"
