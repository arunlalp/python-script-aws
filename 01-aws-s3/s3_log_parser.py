import re
from datetime import datetime

def parse_s3_access_log(log_entry):
    log_pattern = re.compile(
        r'(?P<request_id>\S+) (?P<bucket>\S+) \[(?P<timestamp>[^\]]+)\] (?P<remote_ip>\S+) (?P<requester>\S+) (?P<request_id2>\S+) (?P<operation>\S+) (?P<key>\S+) "(?P<request_uri>[^"]+)" (?P<status>\d+) (?P<error>\S+) (?P<bytes_sent>\d+) (?P<object_size>\S+) (?P<total_time>\d+) (?P<turn_around_time>\S+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)" (?P<version_id>\S+) (?P<host_id>\S+) (?P<signature_version>\S+) (?P<cipher_suite>\S+) (?P<auth_type>\S+) (?P<host_header>\S+) (?P<tls_version>\S+) (?P<additional_details>\S+)'
    )

    match = log_pattern.match(log_entry)

    if match:
        log_data = match.groupdict()
        log_data['timestamp'] = datetime.strptime(log_data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
        return log_data
    else:
        return None

def main():
    log_entry = input("Enter the S3 access log entry: ")
    log_data = parse_s3_access_log(log_entry)

    if log_data:
        print("Parsed S3 Access Log Entry:")
        for key, value in log_data.items():
            print(f"{key}: {value}")
    else:
        print("No match found. Please check the log entry format.")

if __name__ == "__main__":
    main()
