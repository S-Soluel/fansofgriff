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
      email = { response[i]['EmailAddress'], } 
      temp.append(email)
   print(temp)
   return temp

def send_email(template_name, template_data):
   response = ses.send_templated_email(
      Source = 'fansofgriff51@gmail.com',
      Destination = {
         'CcAddresses': 
            get_subscribers('OPT_IN')
                    },
      ReplyToAddresses = [
         'fansofgriff51@gmail.com'
      ],
      Template = template_name,
      # finish getting this to work
        # such as Griff_Sighting
   )
   print(response)

# unsubscribe('sam.solheim@drake.edu')
# subscribe('sam.solheim@drake.edu', 'Sam', 'Solheim')

def get_contact(email):
   response = sesv2.get_contact(
   ContactListName = 'Griff_Tracker_Subscribers', EmailAddress = email
   )
   print(response)

get_email_template()

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
TEMPLATE_NAME = 'Griff_Sighting'
SUBJECT_LINE = 'Breaking News: Griff has been Spotted On-Campus'

TEXT_CONTENT = ("Everyone's favorite bulldog is on campus!\r\n"
             "Griff has been spotted on campus, this is not a drill!\r\n"
             "You can see where he is by going to http://trackgriff.hopto.org/.")

HTML_CONTENT = """<html>
<head></head>
<body>
  <h1>Everyone's favorite bulldog is on campus!</h1>
  <p>Hey {{firstname}}, </p>
  <p>Griff has been spotted on campus, this is not a drill! In order to see where he is on campus, please navigate to the website below. </p>
  <p>This beautiful bulldog is almost as elusive as he is majestic, so don't miss the chance to get pictures with him today.</p>
  <a ref="http://trackgriff.hopto.org/">Visit the Griff Tracker website!"
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









