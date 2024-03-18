import boto3

# Create SES client
ses = boto3.client('ses')

response = ses.verify_email_identity(
  EmailAddress = 'sam.solheim@drake.edu'
)

print(response)