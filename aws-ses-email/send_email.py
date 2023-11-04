import boto3

# Initialize the SES client
ses = boto3.client('ses', region_name='us-west-2')  # Use your AWS region

# Specify email details
sender_email = 'email@devopsproject.dev'
recipient_email = 'arunlal@crunchops.com'
subject = 'Test Email'
message = 'This is a test email sent from Amazon SES.'

# Create the email content
email_content = f"Subject: {subject}\nTo: {recipient_email}\nFrom: {sender_email}\n\n{message}"

# Send the email
response = ses.send_raw_email(
    Source=sender_email,
    Destinations=[recipient_email],
    RawMessage={'Data': email_content}
)

print("Email sent successfully!")
