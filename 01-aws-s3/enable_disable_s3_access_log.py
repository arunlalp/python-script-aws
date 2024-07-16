import boto3
from botocore.exceptions import ClientError

def get_bucket_region(bucket_name):
    s3_client = boto3.client('s3')
    bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)
    return bucket_location['LocationConstraint'] if bucket_location['LocationConstraint'] else 'us-east-1'

def enable_disable_logging(bucket_name, log_bucket_name, enable):
    s3_client = boto3.client('s3')
    
    if enable:
        # Enable logging with a different directory for each bucket
        logging_config = {
            'LoggingEnabled': {
                'TargetBucket': log_bucket_name,
                'TargetPrefix': f'{bucket_name}/'
            }
        }
        
        try:
            s3_client.put_bucket_logging(
                Bucket=bucket_name,
                BucketLoggingStatus=logging_config
            )
            print(f"Server access logging enabled for bucket '{bucket_name}'. Logs will be stored in '{log_bucket_name}/{bucket_name}/'.")
        except ClientError as e:
            print(f"Failed to enable logging for bucket '{bucket_name}': {e}")
    else:
        # Disable logging
        try:
            s3_client.put_bucket_logging(
                Bucket=bucket_name,
                BucketLoggingStatus={}
            )
            print(f"Server access logging disabled for bucket '{bucket_name}'.")
        except ClientError as e:
            print(f"Failed to disable logging for bucket '{bucket_name}': {e}")

# Initialize a session using Amazon S3
s3_client = boto3.client('s3')

# Specify the logging buckets for each region
logging_buckets = {
    'us-east-1': 'US_EAST_1_TARGET_BUCKET',
    'us-west-2': 'US_WEST_1_TARGET_BUCKET',
    # Add other regions and their logging buckets here
}

# Get the list of all buckets
response = s3_client.list_buckets()

print("Select action for each bucket:")
print("1. Enable logging")
print("2. Disable logging")
action_choice = input("Enter your choice (1 or 2): ")

for bucket in response['Buckets']:
    bucket_name = bucket['Name']
    
    # Get the region of the current bucket
    bucket_region = get_bucket_region(bucket_name)
    
    # Skip the log buckets themselves to avoid infinite loop of logging
    if bucket_name in logging_buckets.values():
        continue
    
    # Get the logging bucket for the current region
    log_bucket_name = logging_buckets.get(bucket_region)
    if not log_bucket_name:
        print(f"No logging bucket configured for region '{bucket_region}'. Skipping bucket '{bucket_name}'.")
        continue
    
    # Enable or disable logging based on user choice
    if action_choice == '1':
        enable_disable_logging(bucket_name, log_bucket_name, enable=True)
    elif action_choice == '2':
        enable_disable_logging(bucket_name, log_bucket_name, enable=False)
    else:
        print("Invalid choice. Exiting.")
        break
