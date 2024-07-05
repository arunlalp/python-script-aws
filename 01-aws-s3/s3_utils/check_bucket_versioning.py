import boto3

def check_bucket_versioning(bucket_name):
    s3_client = boto3.client('s3')
    
    try:
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        if 'Status' in versioning and versioning['Status'] == 'Enabled':
            return True
        else:
            return False
    except Exception as e:
        print(f"Could not retrieve versioning status for bucket '{bucket_name}': {e}")
