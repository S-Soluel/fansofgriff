import boto3

# Create SES client
ses = boto3.client('ses')


#response = ses.verify_email_identity(
#  EmailAddress = 'maddie.backhaus@drake.edu'
#)
# email-smtp.us-east-2.amazonaws.com

#response = ses.send_custom_verification_email(
#    EmailAddress = 'maddie.backhaus@drake.edu', 
#    TemplateName = 'EmailVerification'
#)



response = ses.list_templates(
  MaxItems=10
)

print(response)
