import boto3

# Create SES client
ses = boto3.client('ses')



def listTemplates():
    response = ses.list_templates(
  MaxItems=10
)
    print(response)


# Create SES client
ses = boto3.client('ses')

TEMPLATE_NAME = 'Griff_Sighting'
SUBJECT_LINE = 'Breaking News: Griff has been Spotted On-Campus'

TEXT_CONTENT = ("Everyone's favorite bulldog is on campus!\r\n"
             "Griff has been spotted on campus, this is not a drill!\r\n"
             "You can see where he is by going to http://trackgriff.hopto.org/.")

HTML_CONTENT = """<html>
<head></head>
<body>
  <h1>Everyone's favorite bulldog is on campus!</h1>
  <p>Griff has been spotted on campus, this is not a drill! In order to see where he is on campus, please navigate to the website below. </p>
  <p>This beautiful bulldog is almost as elusive as he is majestic, so don't miss this chance to get pictures with him today.</p>
  <a ref="http://trackgriff.hopto.org/">Visit the Griff Tracker website!"
</body>
</html>
            """     




response = ses.create_template(
  Template = {
    'TemplateName' : TEMPLATE_NAME,
    'SubjectPart'  : SUBJECT_LINE,
    'TextPart'     : TEXT_CONTENT,
    'HtmlPart'     : HTML_CONTENT
  }
)


print(response)




