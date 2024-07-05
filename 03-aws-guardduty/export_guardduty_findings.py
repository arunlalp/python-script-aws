import boto3
import json
import csv
import os

# Specify the region
REGION = 'us-west-2'  # Replace with your desired region

# Initialize Boto3 client for GuardDuty with a specified region
client = boto3.client('guardduty', region_name=REGION)

def list_detectors():
    response = client.list_detectors()
    return response['DetectorIds']

def list_findings(detector_id):
    findings = []
    response = client.list_findings(DetectorId=detector_id)
    finding_ids = response['FindingIds']
    
    if finding_ids:
        response = client.get_findings(DetectorId=detector_id, FindingIds=finding_ids)
        findings.extend(response['Findings'])
    
    return findings

def export_findings_to_json(findings, file_path):
    with open(file_path, 'w') as f:
        json.dump(findings, f, indent=4)

def export_findings_to_csv(findings, file_path):
    if not findings:
        return
    
    keys = findings[0].keys()
    with open(file_path, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(findings)

def main():
    detectors = list_detectors()
    all_findings = []

    for detector_id in detectors:
        findings = list_findings(detector_id)
        all_findings.extend(findings)
    
    # Export findings to JSON
    json_file_path = os.path.join(os.getcwd(), f'guardduty_findings_{REGION}.json')
    export_findings_to_json(all_findings, json_file_path)
    print(f'Findings exported to {json_file_path}')
    
    # Export findings to CSV
    csv_file_path = os.path.join(os.getcwd(), f'guardduty_findings_{REGION}.csv')
    export_findings_to_csv(all_findings, csv_file_path)
    print(f'Findings exported to {csv_file_path}')

if __name__ == "__main__":
    main()
