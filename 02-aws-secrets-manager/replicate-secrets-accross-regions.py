import boto3
import base64
from botocore.exceptions import ClientError

# Initialize clients for the source and target regions
source_region = 'us-west-2'
target_region = 'us-east-1'

source_client = boto3.client('secretsmanager', region_name=source_region)
target_client = boto3.client('secretsmanager', region_name=target_region)

# List all secrets in the source region
try:
    paginator = source_client.get_paginator('list_secrets')
    for page in paginator.paginate():
        for secret in page['SecretList']:
            secret_name = secret['Name']
            try:
                response = source_client.get_secret_value(SecretId=secret_name)
                
                if 'SecretString' in response:
                    secret_value = response['SecretString']
                else:
                    secret_value = base64.b64decode(response['SecretBinary'])
                
                # Check if the secret already exists in the target region
                try:
                    target_client.describe_secret(SecretId=secret_name)
                    print(f"The secret '{secret_name}' already exists in the target region '{target_region}'.")
                except target_client.exceptions.ResourceNotFoundException:
                    # Create the secret in the target region
                    target_client.create_secret(
                        Name=secret_name,
                        SecretString=secret_value
                    )
                    print(f"The secret '{secret_name}' has been successfully replicated to the target region '{target_region}'.")
            except ClientError as e:
                print(f"An error occurred while processing the secret '{secret_name}': {e}")
except ClientError as e:
    print(f"An error occurred while listing secrets: {e}")

