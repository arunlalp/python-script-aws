import boto3
import json

# Initialize the KMS client
kms_client = boto3.client('kms')

# Replace with your KMS key ID
key_id = '6a5a6615-6413-412c-9438-617303faf2ba'

def get_key_details(key_id):
    # Describe the key
    key_details = kms_client.describe_key(KeyId=key_id)['KeyMetadata']
    
    # Get the key policy
    policy = kms_client.get_key_policy(KeyId=key_id, PolicyName='default')['Policy']
    
    # List aliases associated with the key
    aliases = kms_client.list_aliases(KeyId=key_id)['Aliases']
    
    # List grants associated with the key
    grants = kms_client.list_grants(KeyId=key_id)['Grants']

    return {
        "Key Details": {
            "Key ID": key_details['KeyId'],
            "ARN": key_details['Arn'],
            "Key State": key_details['KeyState'],
            "Creation Date": key_details['CreationDate'].strftime("%Y-%m-%d %H:%M:%S"),
            "Key Manager": key_details['KeyManager'],
            "Description": key_details.get('Description', 'No Description'),
            "Key Usage": key_details['KeyUsage'],
            "Key Policy": json.loads(policy)
        },
        "Aliases": [{"Alias Name": alias['AliasName'], "Alias ARN": alias['AliasArn']} for alias in aliases],
        "Grants": [
            {
                "Grant ID": grant['GrantId'],
                "Grantee Principal": grant['GranteePrincipal'],
                "Creation Date": grant['CreationDate'].strftime("%Y-%m-%d %H:%M:%S"),
                "Operations": grant['Operations']
            } for grant in grants
        ]
    }

def print_key_info(key_info):
    print("KMS Key Information:")
    print("--------------------")
    
    # Print Key Details
    print("Key Details:")
    for key, value in key_info["Key Details"].items():
        if key == "Key Policy":
            print(f"  {key}:")
            print(json.dumps(value, indent=4))
        else:
            print(f"  {key}: {value}")
    
    # Print Aliases
    print("\nAliases:")
    for alias in key_info["Aliases"]:
        print(f"  Alias Name: {alias['Alias Name']}")
        print(f"  Alias ARN: {alias['Alias ARN']}\n")
    
    # Print Grants
    print("Grants:")
    if key_info["Grants"]:
        for grant in key_info["Grants"]:
            print(f"  Grant ID: {grant['Grant ID']}")
            print(f"  Grantee Principal: {grant['Grantee Principal']}")
            print(f"  Creation Date: {grant['Creation Date']}")
            print(f"  Operations: {', '.join(grant['Operations'])}\n")
    else:
        print("  No Grants associated with this key.")

if __name__ == "__main__":
    key_info = get_key_details(key_id)
    print_key_info(key_info)
