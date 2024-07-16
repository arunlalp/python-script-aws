import boto3
import json
from botocore.exceptions import ClientError

# Replace with your AWS account ID
aws_account_id = "AWS_ACCOUNT_ID"

# Log bucket names per region
log_buckets = {
    'us-east-1': 'US_EAST_1_TARGET_BUCKET',
    'us-west-2': 'US_WEST_1_TARGET_BUCKET',
}

def enable_logging(s3_client, source_bucket, target_bucket):
    try:
        s3_client.put_bucket_logging(
            Bucket=source_bucket,
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': target_bucket,
                    'TargetPrefix': f'{source_bucket}/'
                }
            }
        )
        print(f"Enabled logging for {source_bucket} to {target_bucket}")
    except ClientError as e:
        print(f"Error enabling logging for {source_bucket}: {e}")

def update_bucket_policy(s3_client, target_bucket):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "logging.s3.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{target_bucket}/*",
                "Condition": {
                    "StringEquals": {
                        "aws:SourceAccount": aws_account_id
                    }
                }
            }
        ]
    }

    try:
        s3_client.put_bucket_policy(
            Bucket=target_bucket,
            Policy=json.dumps(policy)
        )
        print(f"Updated policy for {target_bucket}")
    except ClientError as e:
        print(f"Error updating policy for {target_bucket}: {e}")

def main():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()

    for region in log_buckets.keys():
        s3_client = boto3.client('s3', region_name=region)
        log_bucket = log_buckets[region]
        
        # Update policy for the log bucket
        update_bucket_policy(s3_client, log_bucket)

        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            bucket_region = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            if bucket_region is None:
                bucket_region = 'us-east-1'

            if bucket_region == region and bucket_name != log_bucket:
                enable_logging(s3_client, bucket_name, log_bucket)

if __name__ == "__main__":
    main()
