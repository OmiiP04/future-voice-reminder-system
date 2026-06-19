import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VoiceReminders')

ses = boto3.client('ses')

SENDER = "om4201598@gmail.com"
RECIPIENT = "om4201598@gmail.com"

def lambda_handler(event, context):

    reminder_id = event.get("reminder_id", "N/A")

    response = table.get_item(
        Key={
            "reminder_id": reminder_id
        }
    )

    item = response.get("Item", {})

    message = item.get("message", "No message found")
    audio_url = item.get("audio_url", "No audio URL found")

    print("Reminder ID:", reminder_id)
    print("Message:", message)
    print("Audio URL:", audio_url)
    
    email_response = ses.send_email(
        Source=SENDER,
        Destination={
            'ToAddresses': [RECIPIENT]
        },
        Message={
            'Subject': {
                'Data': '🔔 Future Voice Reminder'
            },
            'Body': {
                'Text': {
                    'Data': f"""
🔔 Future Voice Reminder

Reminder ID:
{reminder_id}

Message:
{message}

Audio Reminder:
{audio_url}
"""
                }
            }
        }
    )

    print("Email sent:", email_response)

    return {
        "statusCode": 200,
        "body": json.dumps("Email Sent Successfully")
    }