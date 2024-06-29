import boto3
from datetime import datetime, timedelta

# Initialize boto3 clients
efs_client = boto3.client('efs')
cloudwatch_client = boto3.client('cloudwatch')

# Get the list of all EFS file systems
efs_file_systems = efs_client.describe_file_systems()
file_system_ids = [fs['FileSystemId'] for fs in efs_file_systems['FileSystems']]

# Function to get EFS size from CloudWatch
def get_efs_size(file_system_id):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EFS',
        MetricName='TotalIOBytes',
        Dimensions=[
            {
                'Name': 'FileSystemId',
                'Value': file_system_id
            },
        ],
        StartTime=datetime.utcnow() - timedelta(days=1),
        EndTime=datetime.utcnow(),
        Period=86400,
        Statistics=['Sum']
    )
    if response['Datapoints']:
        size_in_bytes = response['Datapoints'][0]['Sum']
        size_in_kib = size_in_bytes / 1024
        return size_in_kib
    else:
        return 0

# Enable automatic backups and print file system size
for file_system_id in file_system_ids:
    # Enable automatic backups
    response = efs_client.put_backup_policy(
        FileSystemId=file_system_id,
        BackupPolicy={
            'Status': 'ENABLED'
        }
    )
    # Get EFS size
    size = get_efs_size(file_system_id)
    print(f"EFS File System ID: {file_system_id}, Size: {size:.2f} KiB, Automatic backup enabled")
