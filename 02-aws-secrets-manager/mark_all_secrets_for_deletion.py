import boto3
from botocore.exceptions import ClientError

# Initialize client for the specified region
region = 'us-east-1'
client = boto3.client('secretsmanager', region_name=region)

# List all secrets in the specified region
try:
    paginator = client.get_paginator('list_secrets')
    for page in paginator.paginate():
        for secret in page['SecretList']:
            secret_name = secret['Name']
            try:
                # Delete the secret with a 30-day recovery period
                client.delete_secret(
                    SecretId=secret_name,
                    RecoveryWindowInDays=30
                )
                print(f"The secret '{secret_name}' has been marked for deletion with a 30-day recovery period.")
            except ClientError as e:
                print(f"An error occurred while deleting the secret '{secret_name}': {e}")
except ClientError as e:
    print(f"An error occurred while listing secrets: {e}")

