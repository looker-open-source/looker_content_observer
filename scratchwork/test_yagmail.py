import yagmail
import os

"""
Scratchwork: Code to test the yagmail SMTP
"""

user_email = os.environ.get('user_email')
password = os.environ.get('gmail_password')

yag = yagmail.SMTP(user=user_email,
                   password=password)

contents = [
    "This is the body, and here is just text http://somedomain/image.png",
    "You can find an audio file attached.", '/local/path/to/song.mp3'
]
to_email = "ryanrezvani@google.com"
file_loc = "/Users/ryanrezvani/Downloads/another_test.xlsx"
yag.send(to_email, 'Test Email', contents,attachments=file_loc)