import boto3

def enable_bucket_versioning(bucket_name):
    s3_client = boto3.client('s3')

    try:
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
        print(f"Versioning has been enabled for bucet '{bucket_name}'")
    except Exception as e:
        print(f"Could not enable versioning for bucket '{bucket_name}': {e}")
    
    