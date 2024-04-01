import boto3
from flask import json

# Create SES client
ses = boto3.client('ses')
# Create SES V2 API client
sesv2 = boto3.client('sesv2')

# After messing around with it a bit, it seems like there are some operations that only work
# for SES or SES V2 respectively. 


def listTemplates():
    response = ses.list_templates(MaxItems=10)
    print(response)

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
  print(response)

def unsubscribe(email):
   response = sesv2.delete_contact(
      ContactListName = 'Griff_Tracker_Subscribers',
      EmailAddress = email
   )
   print(response)

def get_email_template():
   response = sesv2.get_email_template(
      TemplateName='Griff_Sighting'
   )
   print(response)


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
   print(temp)
   return temp

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
  <a ref="http://trackgriff.hopto.org/">Visit the Griff Tracker website!</a>
  </div>
</body>
</html>
"""     

# update_template(TEMPLATE_NAME, SUBJECT_LINE, TEXT_CONTENT, HTML_CONTENT)
# get_email_template()


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

# get_subscribers('OPT_IN')
# get_email_template()

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

# send_email('Griff_Sighting')

# response = update_template(TEMPLATE_NAME, SUBJECT_LINE, TEXT_CONTENT, HTML_CONTENT)


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

      response = ses.send_templated_email(
      Source = 'Fans of Griff <fansofgriff51@gmail.com>',
      Destination = {'BccAddresses': [temp_email]},
      Template = template_name,
      # such as Griff_Sighting
      TemplateData = json.dumps({'firstname': temp_fn})
      )
   print(response)

# unsubscribe('sam.solheim@drake.edu')
# subscribe('maddie.backhaus@drake.edu', 'Maddie', 'Backhaus')
# send_email('Griff_Sighting')