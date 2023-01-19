# cloud_testing
Contains Following Repos:
- action_api_testing repo: Looker Action API + Cloud Functions to club together csv's into a single Excel file

## Repo: action_api_testing
### Overview
Repo uses the Looker Action API to create a custom [Action](https://developers.looker.com/actions/overview/) within Looker. This action uses [GCP's Cloud Function](https://cloud.google.com/functions) to transform the combined csv zip file into a single Excel (each csv becomes a new named sheet within the Excel) and then uses the [Sendgrid API](https://sendgrid.com/solutions/email-api/) to email the newly created  Excel file to a recipient. 

### Functions
  - **list**: Entry point, informs Looker there is a custom action to perform
  - **form**: Specifies the user inputs (i.e. create a form for a user to enter in an e-mail address etc..)
  - **execute**: Uses the inputs from the form to execute an action, in this case to club the csv zip file together and email it to a user

### Example of Action
For example, I have a Dashboard with 3 tiles (New Users by Signup Date, User Demo - Age, and Product Data):
![Sample Dashboard](/action_api_testing/action_screenshots/action_example_3.png)


I can use the *Schedule Delivery* to trigger the custom Action, called **"Email Combined CSV as Single Excel File"** and asks users to input in an e-mail address as well as a name for the Excel File. 
![Schedule Action](/action_api_testing/action_screenshots/action_example_1.png)

Users will then get an email with an Single Excel FIle where the elements of the dashboard / tiles get turned into Excel sheets within the same file: 
![Schedule Action](/action_api_testing/action_screenshots/action_example_2.png)


### Notes/Further Features
**On modifying the Excel File**: 
By modifying the **execute** function, we can modify the process of creating the Excel file to add custom headers/formatting as needed either by coding the modification into the function and/or pulling a template from a GCS Cloud Storage Bucket and inserting in the data to that template.  

**On the Sendgrid API**: 
Another other SMTP service can be used. Sendgrid was used purely for testing purposes, you can swap in a gmail and/or Outlook account just as easily. 


## Docs/Resources
General Docs:
- [Looker Actions Overivew](https://developers.looker.com/actions/overview/)
- [Looker Action API Overview](https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint)
- [GCP Cloud Function Overiew](https://cloud.google.com/functions)
- [Example of How to Write an Action to BigQuery](https://community.looker.com/looker-api-77/write-the-result-of-a-looker-query-to-bigquery-with-cloud-functions-workaround-for-system-activity-etl-28680)

Helpful Articles:
- [Writing files in Cloud Function](https://medium.com/@hpoleselo/writing-files-within-a-cloud-function-tmp-to-the-rescue-a47a6b482758)