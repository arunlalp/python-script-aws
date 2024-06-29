import boto3

# Initialize boto3 client
efs_client = boto3.client('efs')

# Get the list of all EFS file systems
efs_file_systems = efs_client.describe_file_systems()
file_system_ids = [fs['FileSystemId'] for fs in efs_file_systems['FileSystems']]

# Enable automatic backups for each EFS file system
for file_system_id in file_system_ids:
    response = efs_client.put_backup_policy(
        FileSystemId=file_system_id,
        BackupPolicy={
            'Status': 'ENABLED'
        }
    )
    print(f"Automatic backup enabled for EFS file system: {file_system_id}")
