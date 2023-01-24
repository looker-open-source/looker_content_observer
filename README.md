**Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose. Your use of it is subject to your agreement with Google.** 
# cloud_testing
**Contains Following Repos**:
- **action_api_testing repo**: Looker Action API + Cloud Functions to club together csv's into a single Excel file
- **scratchwork**: Repo for scratchwork and testing code.

## **Repo: action_api_testing**
### Overview
Repo uses the Looker Action API to create a custom [Action](https://developers.looker.com/actions/overview/) within Looker. This action uses [GCP's Cloud Function](https://cloud.google.com/functions) to transform the combined csv zip file into a single Excel (each csv becomes a new named sheet within the Excel) and then uses a [GMAIL SMTP](https://pypi.org/project/yagmail/) to email the newly created  Excel file to a recipient. 

### Functions
  - **list**: Entry point, informs Looker there is a custom action to perform
  - **form**: Specifies the user inputs (i.e. create a form for a user to enter in an e-mail address etc..)
  - **execute**: Uses the inputs from the form to execute an action, in this case to club the csv zip file together and email it to a user

### Example of Action
For example, I have a Dashboard with 3 tiles (New Users by Signup Date, User Demo - Age, and Product Data):
![Sample Dashboard](/action_api_testing/action_screenshots/action_example_3.png)

I can use the *Schedule Delivery* to trigger the custom Action, called **"Email Combined CSV as Single Excel File"** and asks users to input in an e-mail address as well as a name for the Excel File. 
![Schedule Action](/action_api_testing/action_screenshots/action_example_1.png)

Users will then get an email with a single excel file whose name is defined by the inputs from the "Name of Excel File" form defined within Looker:
![Sample Email](/action_api_testing/action_screenshots/action_example_2.png)
**Note**: I am using the gmail SMTP but any SMTP service can be used. 

Each sheet of the Excel File will map to a tile from the dashboard: 
![Downloaded Excel File](/action_api_testing/action_screenshots/action_example_4.png)
**Note**: The function uses an excel template to add formatting and appends the data component below the formatting.

### Further Features
**On modifying the Excel File**: 
By modifying the **execute** function, we can modify the process of creating the Excel file to add custom headers/formatting as needed either by coding the modification into the function and/or pulling a template from a GCS Cloud Storage Bucket and inserting in the data to that template.  

**On the SMTP**: 
Another other SMTP service can be used. Sendgrid and yagmail were used for testing purposes, you can swap in an Outlook account just as easily. 

## Docs/Resources
General Docs:
- [Looker Actions Overivew](https://developers.looker.com/actions/overview/)
- [Looker Action API Overview](https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint)
- [GCP Cloud Function Overiew](https://cloud.google.com/functions)
- [Example of How to Write an Action to BigQuery](https://community.looker.com/looker-api-77/write-the-result-of-a-looker-query-to-bigquery-with-cloud-functions-workaround-for-system-activity-etl-28680)

Helpful Articles:
- [Writing files in Cloud Function](https://medium.com/@hpoleselo/writing-files-within-a-cloud-function-tmp-to-the-rescue-a47a6b482758)
- [Using openpyxl to read an excel file](https://stackoverflow.com/questions/69684388/django-open-excel-xlsx-with-openpyxl-from-google-cloud-storage)


## Repo: action_api_testing

### Overview
Repo contains scratchwork code for various tests. Code is not in managed state and should be ignored.