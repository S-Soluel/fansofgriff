import boto3

# Create SES client
ses = boto3.client('ses')


#response = ses.verify_email_identity(
#  EmailAddress = 'sam.solheim@drake.edu'
#)
# email-smtp.us-east-2.amazonaws.com

response = ses.send_custom_verification_email(
    EmailAddress = 'samsolheim06@gmail.com', 
    TemplateName = 'EmailVerification'
)

print(response)