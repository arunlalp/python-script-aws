import boto3
from .check_bucket_versioning import check_bucket_versioning
from .enable_bucket_versioning import enable_bucket_versioning

def list_buckets():
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            if not check_bucket_versioning(bucket_name):
                enable_bucket_versioning(bucket_name)
    except Exception as e:
        print(f"Could not list buckets: {e}")
