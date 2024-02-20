# Automation of ETL (Extract,Trasform,Load) using Lambda

Amazon S3 event triggers the automatic initiation of AWS Lambda functions or other AWS services in response to events within an Amazon S3 bucket. These events include actions such as object creation, deletion, or modification. S3 event triggers facilitate real-time processing and automation, allowing developers to build scalable and event-driven architectures.

Within this project, our focus is on activating S3 events, specifically those associated with object creation, to trigger a Lambda function. The Lambda function is designed to transform the data within files uploaded to an S3 bucket. Once transformation is done, data is inserted into an Aurora Database.

## Steps to execute

1.	Access the AWS console, navigate to S3, and create an S3 bucket using default configurations with an appropriate name.

   ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/Bucket_created.jpg)

2.	Create a Serverless Aurora Database cluster programmatically using Python and Boto3.

   ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/Db-cluster_created.jpg)

  ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/db_cluster_created.jpg)

3.	Once the database is created, open Query Editor from RDS console and connect to your database created by entering appropriate database username and password.In the editor run a query to create the billing_data table.

   ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/table_created.jpg)

4.	Next to create a Lambda function,  navigate to Lambda console. Click on "Create function."Choose a meaningful name for your Lambda function, specify the runtime as Python 3.9, and create a new role.

   ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/lambda_created.jpg)

5.	For local testing of Lambda functions, download the functions to Cloud9 environment, create event.json and template .yaml files. Use below code from terminal to test the functions.

   ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/Local_invoke_command.jpeg)

6.	Upon successful local testing, upload the Lambda function code from Cloud9 to AWS Lambda.

7.	Grant Permissions to Lambda to access S3 bucket, secrets from Secret Manager and also for RDS execution . Attach IAM policies to the Lambda Execution Role to provide these permissions.

    ![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/lambda_permissions.jpg)

8.	Create a trigger from the Lambda console by clicking on ‘Add Trigger’. Select S3 as source and also select appropriate  S3 bucket from which trigger has to be created. Select the Event type as ‘PUT’.

9.	Upload the file into S3 bucket which will trigger the lambda function.

   
## Result

The transformed data from S3 file is inserted into billing_data table.

![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/data_inserted_db1.jpg)

![alt text](https://github.com/pratheekshavrao/S3_DataTransformation_AuroraStorage/blob/master/images/data_inserted_db2.jpg)
