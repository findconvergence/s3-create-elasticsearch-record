# s3-create-elasticsearch-record
This Python 3.6 package for AWS Lambda creates a record in AWS Elasticsearch when sent an 'ObjectCreate' event from an s3 bucket. 
* Set up as many s3 bucket triggers as you like.
* Also creates a new index in Elasticsearch if you don't already have one.


##Credits:
Credit to Amit Sharma (@amitksh44) for the [original scripts](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/) for Python 2.7.  This update allows you to use Python 3.6 and the latest Elasticsearch build to keep a dynamic catalog of your Data Lake objects in AWS S3.  

See the accompanying repo to remove records.

##Requirements:
AWS S3 bucket(s)
AWS Lambda
AWS Elasticsearch endpoint

All required modules are currently included in the AWS Lambda environment, except for Elasticsearch.  

>> pip install elasticsearch
(This will install urllib as well)
