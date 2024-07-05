import boto3

def create_backup_plan():
    backup_client = boto3.client('backup')

    try:
        response = backup_client.create_backup_plan(
            BackupPlan={
                'BackupPlanName': 'S3BackupPlan',
                'Rules': [
                    {
                        'RuleName': 'DailyBackupRule',
                        'TargetBackupVaultName': 'Default',
                        'ScheduleExpression': 'string',
                        'StartWindowMinutes': 123,
                        'CompletionWindowMinutes': 123,
                        'Lifecycle': {
                            'MoveToColdStorageAfterDays': 123,
                            'DeleteAfterDays': 123,
                            'OptInToArchiveForSupportedResources': True|False
                        },
                        'RecoveryPointTags': {
                            'string': 'string'
                        },
                        'CopyActions': [
                            {
                                'Lifecycle': {
                                    'MoveToColdStorageAfterDays': 123,
                                    'DeleteAfterDays': 123,
                                    'OptInToArchiveForSupportedResources': True|False
                                },
                                'DestinationBackupVaultArn': 'string'
                            },
                        ],
                        'EnableContinuousBackup': True|False,
                        'ScheduleExpressionTimezone': 'string'
                    },
                ],
                'AdvancedBackupSettings': [
                    {
                        'ResourceType': 'string',
                        'BackupOptions': {
                            'string': 'string'
                        }
                    },
                ]
            },
            BackupPlanTags={
                'string': 'string'
            },
            CreatorRequestId='string'
        )
        backup_plan_id = response['BackupPlanId']
        print(f"Backup plan created with ID: {backup_plan_id}")
        return backup_plan_id
    except Exception as e:
        print(f"Could not create backup plan: {e}")
        return None