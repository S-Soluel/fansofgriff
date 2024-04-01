# Sam S
# 3/25/24
# Working with the SNS information to see about how we could let people subscribe themselves to the Griff Tracker. 
# Possibly better to do this than specifically the SES version. In this case, each email allows people to unsubscribe if they choose to do so. 
import boto3

sns = boto3.client('sns')

def subscribe(client, email):
    response = client.subscribe(
        TopicArn = 'arn:aws:sns:us-east-2:767397777937:Griff_Sighting',
        Protocol = 'email', Endpoint=email)
    
    print(response)
    return(response)




