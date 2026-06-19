# Future Voice Reminder System

A serverless AWS application that converts reminder text into speech using Amazon Polly, stores MP3 files in Amazon S3, saves metadata in DynamoDB, schedules future reminders using EventBridge Scheduler, and sends automated email notifications with playable voice reminder links via Amazon SES.

## AWS Services Used

 API Gateway
 AWS Lambda
 Amazon Polly
 Amazon S3
 Amazon DynamoDB
 Amazon EventBridge Scheduler
 Amazon SES
 CloudWatch
 IAM

## Architecture

User → API Gateway → Lambda → Polly → S3 → DynamoDB → EventBridge Scheduler → Lambda → SES → Email → MP3 Playback

## Features

 Text-to-Speech Conversion
 Automated Reminder Scheduling
 Email Notifications
 MP3 Audio Storage
 Serverless Architecture
 Event-Driven Workflow

## Technologies

 Python
 Boto3
 AWS Cloud Services
