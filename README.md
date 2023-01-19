# cloud_testing
Contains Following Repos:
- action_api_testing repo: Looker Action API + Cloud Functions to club together csv's into a single Excel file

## Repo: action_api_testing
### Overview
Repo uses the Looker Action API to create a custom Action. This action uses GCP's Cloud Function to transform the combined csv zip file into a single Excel (each csv becomes a new named sheet within the Excel) and then uses the Sendgrid API to email the transfomed Excel file to a recipient. 

### Functions
  - list: Entry point, informs Looker there is a custom action to perform
  - form: Specifies the user inputs (i.e. create a form for a user to enter in an e-mail address etc..)
  - execute: Uses the inputs from the form to execute an action, in this case to club the csv zip file together and email it to a user

## Docs/Resources
General Docs:
- [Looker Action API Overview](https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint)
- [GCP Cloud Function Overiew](https://cloud.google.com/functions)
- [Example of How to Write an Action to BigQuery](https://community.looker.com/looker-api-77/write-the-result-of-a-looker-query-to-bigquery-with-cloud-functions-workaround-for-system-activity-etl-28680)

Helpful Articles:
- [Writing files in Cloud Function](https://medium.com/@hpoleselo/writing-files-within-a-cloud-function-tmp-to-the-rescue-a47a6b482758)