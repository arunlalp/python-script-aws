import boto3
import json

# Initialize a session using Amazon Secrets Manager
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name='us-west-2'  # Replace with your AWS region
)

def restore_secrets_from_backup(backup_file):
    try:
        # Read the backup JSON file
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)

        # Restore each secret from the backup
        for secret_data in backup_data:
            secret_id = secret_data['Name']
            secret_description = secret_data.get('Description', '')
            secret_string = secret_data.get('SecretString', None)
            secret_binary = secret_data.get('SecretBinary', None)

            try:
                # Check if secret already exists
                client.describe_secret(SecretId=secret_id)
                
                try:
                    # Update the secret
                    if secret_string:
                        client.update_secret(SecretId=secret_id, SecretString=secret_string, Description=secret_description)
                    elif secret_binary:
                        client.update_secret(SecretId=secret_id, SecretBinary=secret_binary, Description=secret_description)
                    print(f"Updated secret: {secret_id}")
                except client.exceptions.InvalidRequestException as e:
                    # If secret is marked for deletion, restore it first
                    if 'marked for deletion' in str(e):
                        client.restore_secret(SecretId=secret_id)
                        print(f"Restored secret: {secret_id} from deletion. Retrying update...")
                        if secret_string:
                            client.update_secret(SecretId=secret_id, SecretString=secret_string, Description=secret_description)
                        elif secret_binary:
                            client.update_secret(SecretId=secret_id, SecretBinary=secret_binary, Description=secret_description)
                        print(f"Updated secret: {secret_id}")
                    else:
                        raise e
            except client.exceptions.ResourceNotFoundException:
                # Secret does not exist, create it
                create_params = {
                    'Name': secret_id,
                    'Description': secret_description
                }
                if secret_string:
                    create_params['SecretString'] = secret_string
                elif secret_binary:
                    create_params['SecretBinary'] = secret_binary
                client.create_secret(**create_params)
                print(f"Created secret: {secret_id}")

        print(f'Restored secrets from {backup_file}')
    except Exception as e:
        print(f'Error restoring secrets: {e}')

if __name__ == '__main__':
    backup_file = 'secrets_backup_20240702_190035.json'  # Replace with your backup file name
    restore_secrets_from_backup(backup_file)
