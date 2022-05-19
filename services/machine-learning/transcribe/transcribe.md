# Amazon Transcribe

## General info
Audio -> text

Amazon Transcribe is an automatic speech recognition (ASR) service that makes it easy to add speech-to-text capability to applications. 
Amazon Transcribe can process audio files from S3 or via real-time streams.

can analyze audio files stored in S3 and return a text file of the transcribed speech; also support live audio stream to receive a stream of text

* supports FLAC, MP4, WAV, MP3 with time stamps for every word so that we can easily locate the audio in the original 
source by searching for the text
* streaming audio supported (HTTP/2 or websocket) -> french, english, spanish only
* speaker identification: specify number of speakers
* channel identification: two callers could be transcribed separately, merging based on timing of "utterances"
* custom vocabularies
    * vocabulary lists (just a list of special words, names, acronyms)
    * vocabulary tables (can include "SoundsLike", "IPA (international phonetic alphabet)", and "DisplayAs")


## API
Transcribe API is asynchronous because it can last a long time. Calling the API is "fire and forget" with a unique ID and then check the completion until it is finished.

Good practice is object created on S3 -> trigger events for lambda -> lambda process which bucket, which key -> send to transcribe with an ID

```python
import boto3
import uuid

def lambda_handler(event, context):
    record = event['Records'][0]
    s3_bucket = record['s3']['bucket']['name']
    s3_object = record['s3']['object']['key']
    
    s3_path = "s3://" + s3_bucket + "/" + s3_object
    job_name = s3_object + '-' + str(uuid.uuid4())
    
    transcribe = boto3.client('transcribe')
    
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',
        MediaFormat='mp4',
        Media={
            'MediaFileUri': s3_path
        })
        
    return {
        'statusCode': 200,
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }
```

the lambda test event would be
```json
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "2019-08-19T00:40:34.543Z",
      "eventName": "ObjectCreated:Copy",
      "userIdentity": {
        "principalId": "AWS:AIDAQJESG6ASNHUMQS6S"
      },
      "requestParameters": {
        "sourceIPAddress": "119.18.34.112"
      },
      "responseElements": {
        "x-amz-request-id": "5E41409CF7FD3202",
        "x-amz-id-2": "yiedfPHGd9hXMYDc9C29NBYC2hFmmAASL5Vi7RUpnIvEVgqsX5IM2inphFVADsKxvYEXVm9BzY="
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "ODE5NGE3M2ItWFiMS00YmI0LThhMGMtNzM0MjMzN2UxOTE3",
        "bucket": {
          "name": "input-cfst-2176-2d3399f390148ae2eca37b77f663f32f",
          "ownerIdentity": {
            "principalId": "A2E7ZEMFS8ZMW"
          },
          "arn": "arn:aws:s3:::input-cfst-2176-2d3399f390148ae2eca37b77f663f32f"
        },
        "object": {
          "key": "tea.m4a",
          "size": 1228405,
          "eTag": "7a6afa78089383ef7bfd343302560a2",
          "sequencer": "005D59F0025D9258B"
        }
      }
    }
  ]
}
```

The response from the lambda
```json
{
  "TranscriptionJob": {
    "TranscriptionJobName": "tea.m4a-25e5a7d8-f5a4-46ea-87a8-2eccae536085",
    "TranscriptionJobStatus": "IN_PROGRESS",
    "LanguageCode": "en-US",
    "MediaFormat": "mp4",
    "Media": {
      "MediaFileUri": "s3://input-cfst-2176-2d3399f390148ae2eca37b77f663f32f/tea.m4a"
    },
    "StartTime": "2020-04-25 22:43:28.448000+00:00",
    "CreationTime": "2020-04-25 22:43:28.427000+00:00"
  },
  "ResponseMetadata": {
    "RequestId": "fae35c45-89cc-4114-baf0-8fa5303ff053",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "content-type": "application/x-amz-json-1.1",
      "date": "Sat, 25 Apr 2020 22:43:27 GMT",
      "x-amzn-requestid": "fae35c45-89cc-4114-baf0-8fa5303ff053",
      "content-length": "324",
      "connection": "keep-alive"
    },
    "RetryAttempts": 0
  }
}
```

## Use cases
* real time transcription or offline transcription jobs
* transcription of customer service calls
* generating subtitles on audio and video content
* creates a call center monitoring solution that integrates with other services to analyze caller sentiment
* create a solution to enable text search of media with spoken words
* provide a closed captioning solution for online video training

## Custom vocabulary
Can use custom vocabulary to help the service to understand the terminology we are using with the speech

We can upload a text file with the vocabulary in it, the format is one word per line or we can select a file in S3
=> it takes time to process (Pending then Ready status), 2 words was 2 minutes in the example video

## Transcription jobs
We can upload files or use files from S3

## Resources

FAQ: https://aws.amazon.com/transcribe/faqs/

