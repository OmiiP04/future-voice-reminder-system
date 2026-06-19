import json
import boto3
import uuid
import os
from datetime import datetime, timedelta


s3 = boto3.client('s3')
polly = boto3.client('polly')
scheduler = boto3.client('scheduler')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

SEND_REMINDER_ARN = "arn:aws:lambda:ap-south-1:366290348435:function:send-reminder"

SCHEDULER_ROLE_ARN = "arn:aws:iam::366290348435:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_16e3bb3836"


def lambda_handler(event, context):

    if 'body' in event:
        body = json.loads(event['body'])
        message = body.get('message', 'Hello Future Om')
    else:
        message = event.get('message', 'Hello Future Om')

    reminder_id = str(uuid.uuid4())

    response = polly.synthesize_speech(
        Text=message,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

   
    audio_data = response['AudioStream'].read()
    file_name = f"{reminder_id}.mp3"
    audio_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{file_name}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=audio_data,
        ContentType='audio/mpeg'
    )

    table.put_item(
    Item={
        'reminder_id': reminder_id,
        'message': message,
        'audio_file': file_name,
        'audio_url': audio_url
    }
    )

    future_time = datetime.now() + timedelta(minutes=5)


    schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    scheduler.create_schedule(
        Name=f"reminder-{reminder_id}",
        ScheduleExpression=f"at({schedule_time})",
        FlexibleTimeWindow={
            "Mode": "OFF"
        },
        Target={
            "Arn": SEND_REMINDER_ARN,
            "RoleArn": SCHEDULER_ROLE_ARN,
            "Input": json.dumps({
                "reminder_id": reminder_id,
                "message": message
            })
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'MP3 Generated Successfully',
            'reminder_id': reminder_id,
            'scheduled_for': schedule_time
        })
    }