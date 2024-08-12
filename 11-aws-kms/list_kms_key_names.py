import boto3

def list_customer_managed_kms_key_names(region_name):
    # Initialize a session using Boto3 and specify the region
    session = boto3.Session(region_name=region_name)
    kms_client = session.client('kms')

    # List all aliases
    aliases = kms_client.list_aliases()
    
    # Filter for customer-managed keys only (exclude AWS-managed keys)
    customer_managed_key_names = [
        alias['AliasName'] for alias in aliases['Aliases'] 
        if 'TargetKeyId' in alias and not alias['AliasName'].startswith('alias/aws/')
    ]

    return customer_managed_key_names

if __name__ == "__main__":
    # Specify the AWS region
    region = "us-west-2"  # change this to your preferred region

    # Get the list of customer-managed KMS key names (aliases)
    kms_key_names = list_customer_managed_kms_key_names(region)

    # Print the key names
    for name in kms_key_names:
        print(name)
