import boto3
import json
from datetime import datetime

# Initialize a session using Amazon Secrets Manager
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name='us-west-2'  # Replace with your AWS region
)

# Function to list all secrets
def list_secrets(client):
    secrets = []
    paginator = client.get_paginator('list_secrets')
    for page in paginator.paginate():
        secrets.extend(page['SecretList'])
    return secrets

# Function to get secret value and metadata
def get_secret_details(client, secret_id):
    secret_details = client.describe_secret(SecretId=secret_id)
    try:
        secret_value = client.get_secret_value(SecretId=secret_id)
        secret_details['SecretString'] = secret_value.get('SecretString', '')
        secret_details['SecretBinary'] = secret_value.get('SecretBinary', '')
    except client.exceptions.ResourceNotFoundException:
        print(f'Secret {secret_id} not found.')
    return secret_details

# Function to serialize datetime objects to string
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()

def main():
    # Get the current date and time for the backup filename
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'secrets_backup_{current_time}.json'

    # List all secrets
    secrets = list_secrets(client)

    # Get details for each secret
    all_secrets = []
    for secret in secrets:
        secret_id = secret['Name']
        print(f'Backing up secret: {secret_id}')
        secret_details = get_secret_details(client, secret_id)
        all_secrets.append(secret_details)

    # Save all secrets to a backup file
    with open(backup_file, 'w') as f:
        json.dump(all_secrets, f, indent=4, default=datetime_converter)

    print(f'Backup completed. Secrets saved to {backup_file}')

if __name__ == '__main__':
    main()
