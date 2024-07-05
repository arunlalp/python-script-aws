import boto3
import json
from datetime import datetime
from typing import Any

# Specify the region
REGION = 'us-west-2'  # Replace with your desired region

# Initialize Boto3 client for GuardDuty with a specified region
client = boto3.client('guardduty', region_name=REGION)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def list_detectors():
    response = client.list_detectors()
    return response['DetectorIds']

def get_detector_details(detector_id):
    response = client.get_detector(DetectorId=detector_id)
    return response

def get_enabled_features(detector_details):
    features = []

    # Check for specific data sources
    data_sources = detector_details.get('DataSources', {})
    if 'S3Logs' in data_sources.get('S3Logs', {}).get('DataSourceStatus', '') and data_sources['S3Logs']['DataSourceStatus'] == 'ENABLED':
        features.append({'Name': 'S3_DATA_EVENTS', 'Status': 'ENABLED'})

    if 'CloudTrail' in data_sources.get('CloudTrail', {}).get('DataSourceStatus', '') and data_sources['CloudTrail']['DataSourceStatus'] == 'ENABLED':
        features.append({'Name': 'CLOUDTRAIL', 'Status': 'ENABLED'})

    # Check for specific member accounts
    member_accounts = detector_details.get('MemberDataSourceConfigurations', [])
    for member_account in member_accounts:
        if member_account.get('Status') == 'ENABLED':
            features.append({'Name': 'MEMBER_ACCOUNT_REPORT', 'Status': 'ENABLED', 'AccountId': member_account.get('AccountId')})

    # Check for specific service roles
    service_role = detector_details.get('ServiceRole')
    if service_role:
        features.append({'Name': 'SERVICE_ROLE', 'Status': 'ENABLED', 'ServiceRole': service_role})

    return features

def main():
    detectors = list_detectors()
    output_file = f'guardduty_features_{REGION}.json'  # Output file name
    
    with open(output_file, 'w') as f:
        for detector_id in detectors:
            detector_output = {}
            detector_output['DetectorId'] = detector_id
            
            details = get_detector_details(detector_id)
            detector_output['DetectorDetails'] = details
            
            features = get_enabled_features(details)
            detector_output['EnabledFeatures'] = features
            
            # Write detector output to file
            f.write(json.dumps(detector_output, indent=4, cls=CustomJSONEncoder))
            f.write('\n\n')  # Separate detectors with new lines
    
    print(f'GuardDuty features exported to {output_file}')

if __name__ == "__main__":
    main()
