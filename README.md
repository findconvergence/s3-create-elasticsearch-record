# s3-create-elasticsearch-record
This Python 3.6 package for AWS Lambda creates a record in AWS Elasticsearch when sent an 'ObjectCreate' event from an s3 bucket. 
* Set up as many s3 bucket triggers as you like. We can handle it.
* Also creates a new index in Elasticsearch if you don't already have one.


## Thanks:
Credit to Amit Sharma (@amitksh44) for the [original scripts](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/) for Python 2.7.  This update allows you to use Python 3.6 and the latest Elasticsearch build to keep a dynamic catalog of your Data Lake objects in AWS S3.  

See the accompanying repo to remove records.

## Requirements:
* AWS S3 bucket
* AWS Lambda 
* AWS Elasticsearch endpoint

## Configuration 
* First time packaging a Python script for Lambda?  [Read this guide.](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/)
* Update your AWS Lambda endpoint under *user constants* in **lambda_function.py** (Note the AWS default port for Elasticsearch is 80.)
* All required modules are currently included in the AWS Lambda environment, except for Elasticsearch. 
..* **pip install elasticsearch -t .** will update Elasticsearch locally (and install urllib as well.)
* Run **chmod -R 755** on all files
* Zip and upload file to your Lambda function.
