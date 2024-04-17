import boto3
from botocore.config import Config
from flask import json


my_config = Config(
    region_name = 'us-east-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Create SES client
ses = boto3.client('ses', config=my_config)
# Create SES V2 API client
sesv2 = boto3.client('sesv2', config=my_config)

# After messing around with it a bit, it seems like there are some operations that only work
# for SES or SES V2 respectively. 
# Plus side --> you can call to these apis and get the same information from SES. 

def listTemplates():
    response = ses.list_templates(MaxItems=10)
    print(response)

def verify_id(email):
   response = ses.verify_email_identity(EmailAddress = email)
   #print(response)
   return(response)


# following function uses sesv2 api call to "create_contact"
# Theoretically should allow us to get emails by 'subscribing' to an email list
# Need to figure out why it says Joe and Maddie M are resulting in errors that
# they "are not verified." This should have been fixed since I moved away from "create_identities"
def subscribe(email, firstname, lastname):
  attributes_data = {
        'firstname': firstname,
        'lastname': lastname }
  attributes_data_str = json.dumps(attributes_data)
  
  response = sesv2.create_contact(
     ContactListName = 'Griff_Tracker_Subscribers',
     EmailAddress = email,
     TopicPreferences = [
        {
           'TopicName': 'GriffWatch',
           'SubscriptionStatus': 'OPT_IN'
        }
     ],
     UnsubscribeAll = False,
     AttributesData=attributes_data_str
  )
  #print(response)
  verify_id(email)

# This function allows someone to input their email address, and then their
# contact in SES will be deleted. 
def unsubscribe(email):
   response = sesv2.delete_contact(
      ContactListName = 'Griff_Tracker_Subscribers',
      EmailAddress = email
   )
   #print(response)

# Returns the json parameters that are associated with the "Griff__Sighting" email template. 
def get_email_template():
   response = sesv2.get_email_template(
      TemplateName='Griff_Sighting'
   )
   print(response)

# This function simply returns the email addresses of all subscribers
# Used as a helper function to get a list of emails, which is later used
# to correctly specify who has opted-in for emails about the dog. 
def get_subscribers(filter):
   # Need to iteratively get the list of subscribers from the JSON
   temp = []
   
   response = sesv2.list_contacts(
      ContactListName = 'Griff_Tracker_Subscribers',
      Filter={
         'FilteredStatus':filter
      }
   )
   response = response['Contacts']
   for i in range(len(response)):
      email = response[i]['EmailAddress']
      temp.append(email)
   #print(temp)
   return temp

# The following strings are for messing with the email templates.
TEMPLATE_NAME = 'Griff_Sighting'
SUBJECT_LINE = 'Breaking News: Griff has been Spotted On-Campus'

TEXT_CONTENT = ("Everyone's favorite bulldog is on campus!\r\n"
             "Griff has been spotted on campus, this is not a drill!\r\n"
             "You can see where he is by going to http://trackgriff.hopto.org/.")

HTML_CONTENT = """<html>
<head></head>
<body>
  <div>
  <h1>Everyone's favorite bulldog is on campus!</h1>
  <p>Hey {{firstname}}, </p>
  <p>Griff has been spotted on campus, this is not a drill! In order to see where he is on campus, please navigate to the website below. This beautiful bulldog is almost as elusive as he is majestic, so don't miss the chance to get pictures with him today.</p>
  <a href='http://trackgriff.hopto.org/' target='_blank'>Visit the Griff Tracker website!</a>

  <p>Do you believe you received this email by accident? Are you no longer a fan of Griff? If either of these is the case, please use the following link to unsubscribe:</p>
  <a href='http://trackgriff.hopto.org/unsubscribe'>Unsubscribe</a>
  </div>
</body>
</html>
"""     

## Commented out the code for creating the contact list
"""
response = sesv2.create_contact_list(
   ContactListName = 'Griff_Tracker_Subscribers',
   Topics =[
      {
         'TopicName': 'GriffWatch',
         'DisplayName': 'Griff Watch',
         'Description': 'With a subscription to the Griff Tracker, you can opt-in to receive emails when Griff is spotted on campus!',
         'DefaultSubscriptionStatus': 'OPT_IN'
      }
   ]
)
"""
"""
response = ses.send_templated_email(
   Source='Fans Of Griff <fansofgriff51@gmail.com>',
   Template=TEMPLATE_NAME,
   Destination={
      'BccAddresses': [
         'sam.solheim@drake.edu'
      ], 
   },
   TemplateData = '{"firstname": "Sam"}'
      
)
print(response)
"""

def get_contact(email):
   response = sesv2.get_contact(
   ContactListName = 'Griff_Tracker_Subscribers', EmailAddress = email
   )
   attr_data = json.loads(response['AttributesData'])
   temp_dict = {'EmailAddress': response['EmailAddress'], 'firstname': attr_data['firstname']}
   #print(temp_dict)
   return(temp_dict)

## Need to make a function that will give me a list of dictionaries
def get_subscribers_and_templatedata():
   temp = []
   emails = get_subscribers('OPT_IN')
   # unfortunately, we can't get all the info we need from just one pre-built function.
   # needed to make the 'get_subscribers' function to get a list of emails
   for email in emails:
      contact = get_contact(email)
      temp.append(contact)

   return(temp)

def update_template(name, subject, text_content, html_content):
   response = sesv2.update_email_template(
      TemplateName= name,
      TemplateContent={
        'Subject': subject,
        'Text': text_content,
        'Html': html_content
    }
)
   print(response)

def send_email(template_name):
   # Unfortunately, from what I've seen so far we might just need to have a for loop in this function,
   # and have it make calls to SES for each individual email we want to send in order for them to be customized for 
   # each recipient. :/
   email_list = get_subscribers_and_templatedata()
   # format of the above: 
   # [{'EmailAddress': 'sam.solheim@drake.edu', 'firstname': 'Sam'},
   #  {'EmailAddress': 'maddie.backhaus@drake.edu', 'firstname': 'Maddie'}]

   for person in email_list:
      temp_email = person['EmailAddress']
      temp_fn = person['firstname']
      try:
         response = ses.send_templated_email(
         Source = 'Fans of Griff <fansofgriff51@gmail.com>',
         Destination = {'BccAddresses': [temp_email]},
         Template = template_name,
         # such as Griff_Sighting
         TemplateData = json.dumps({'firstname': temp_fn})
         )
         print(response)
      except:
         print("An error occurred. This Griff Tracker Alert was not sent to: " + temp_email)

# subscribe('samuelmsolheim@gmail.com', 'Test', 'Case')
# unsubscribe('maddie.mcerlean@drake.edu')
# unsubscribe('joe.barnard@drake.edu')
# subscribe('maddie.mcerlean@drake.edu', 'Maddie', 'McErlean')
# subscribe('joe.barnard@drake.edu', 'Joe', 'Barnard')
# send_email('Griff_Sighting')

#update_template(TEMPLATE_NAME, SUBJECT_LINE, TEXT_CONTENT, HTML_CONTENT)
#get_email_template()
