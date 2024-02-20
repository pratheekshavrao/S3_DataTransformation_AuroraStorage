# Automation of ETL (Extract,Trasform,Load) using Lambda

Amazon S3 event triggers the automatic initiation of AWS Lambda functions or other AWS services in response to events within an Amazon S3 bucket. These events include actions such as object creation, deletion, or modification. S3 event triggers facilitate real-time processing and automation, allowing developers to build scalable and event-driven architectures.

Within this project, our focus is on activating S3 events, specifically those associated with object creation, to trigger a Lambda function. The Lambda function is designed to transform the data within files uploaded to an S3 bucket. Once transformation is done, data is inserted into an Aurora Database.
