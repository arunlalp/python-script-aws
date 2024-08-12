import boto3
import json
from datetime import datetime

def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()

def get_kms_keys_details(region_name):
    # Initialize a session using Boto3 and specify the region
    session = boto3.Session(region_name=region_name)
    kms_client = session.client('kms')

    # List all customer-managed keys
    keys = kms_client.list_keys()
    key_details = []

    for key in keys['Keys']:
        # Get key details for each key
        key_info = kms_client.describe_key(KeyId=key['KeyId'])['KeyMetadata']

        # Filter out AWS-managed keys
        if key_info['KeyManager'] == 'CUSTOMER':
            # Get the key's aliases
            aliases = kms_client.list_aliases(KeyId=key['KeyId'])
            key_info['Aliases'] = [alias['AliasName'] for alias in aliases['Aliases']]

            key_details.append(key_info)

    return key_details

def write_to_file(filename, data):
    # Write the JSON output to a file, using the datetime converter
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, default=datetime_converter)

if __name__ == "__main__":
    # Specify the AWS region
    region = "us-west-2"  # change this to your preferred region

    # Get details of all customer-managed keys in the specified region
    kms_details = get_kms_keys_details(region)

    # Write the output to a file
    output_filename = "kms_keys_details.json"
    write_to_file(output_filename, kms_details)

    print(f"Output written to {output_filename}")
