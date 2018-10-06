# s3-create-elasticsearch-record
# Creates an AWS Elasticsearch record when sent an s3 'ObjectCreate' event via AWS Lambda

import json
import urllib
import boto3
from elasticsearch import Elasticsearch

s3 = boto3.client('s3')

# user constants
ES_ENDPOINT = 'xxxx.xxxx.region.es.amazonaws.com' # Your Elasticsearch endpoint URL
ES_PORT = 80 # AWS Elasticsearch port 80; default Elasticsearch port 9200
ES_INDEX = 's3' # Your Elasticsearch index
ES_DOC = 'object' # Your Elasticsearch doc type


def lambda_handler(lambda_event, context):
    print('Received Lambda Event: ' + json.dumps(lambda_event))

    es = connect_elasticsearch(ES_ENDPOINT, ES_PORT)
    s3_result = get_object(lambda_event)
    create_index(es)
    create_record(es, s3_result)


def connect_elasticsearch(ES_ENDPOINT, ES_PORT):
    _es = None
    _es = Elasticsearch(hosts=[{'host': ES_ENDPOINT, 'port': ES_PORT}])

    try:
        _es.ping()
        print('Elasticsearch Connected')
        return _es
    except Exception as e:
        print('Elasticsearch Not Connected - Abort')
        raise e
        exit()


def get_object(lambda_event):
    s3_bucket = lambda_event['Records'][0]['s3']['bucket']['name']
    s3_key = urllib.parse.unquote_plus(lambda_event['Records'][0]['s3']['object']['key'])

    # get object data from s3
    try:
        s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    except Exception as e:
        raise e

    # parse object data
    try:
        result = parse_object(s3_object, s3_bucket, s3_key)
        print('Record: ',result)
        return result
    except Exception as e:
        raise e


def parse_object(s3_object, s3_bucket, s3_key):
    indexcreatedDate = s3_object['LastModified']
    indexBucket = s3_bucket
    indexObjectKey = s3_key
    indexcontent_type = s3_object['ContentType']
    indexcontent_length = s3_object['ContentLength']
    indexmetadata = json.dumps(s3_object['Metadata'])

    parsed = {'createdDate': indexcreatedDate,
              'bucket': indexBucket,
              'objectKey': indexObjectKey,
              'content_type': indexcontent_type,
              'content_length': indexcontent_length,
              'metadata': indexmetadata}

    return json.dumps(parsed, default=str)


def create_index(es):
    created = False
    es_index_body = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0
        },
        'object': {
            'properties': {
                'createdDate': {
                    'type': 'date',
                    'index': True,
                    'format': 'dateOptionalTime'
                },
                'bucket': {
                    'type': 'text',
                    'index': True
                },
                'objectKey': {
                    'type': 'text',
                    'index': True
                },
                'content_type': {
                    'type': 'text',
                    'index': True
                },
                'content_length': {
                    'type': 'long',
                    'index': True
                },
                'metadata': {
                    'type': 'text',
                    'index': True
                }
            }
        }
    }

    try:
        if not es.indices.exists(ES_INDEX):
            es.indices.create(index=ES_INDEX, ignore=400, body=es_index_body) # Ignore 400 ignores 'Index Already Exists' error.
            print('Created Index')
            index_created = True
        else:
            index_created = False
    except Exception as e:
        print(str(e))
    finally:
        return index_created


def create_record(es, s3_result):
    rec_created = True

    try:
        create = es.index(index=ES_INDEX, doc_type=ES_DOC, body=s3_result)
    except Exception as e:
        print(str(e))
        rec_created = False
    finally:
        print('Record Created: ', rec_created)
        return rec_created
