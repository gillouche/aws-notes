# Amazon Simple Notification Service (SNS)

## General Info

fully managed service for publisher-subscriber message and mobile notifications => push mechanism, no polling required

A2A (application to application), A2P (application to person), pub/sub, push based

SNS fanout: publish to topic, multiple SQS queues subscribed (= fanout)
* fanout to Kinesis data firehose
* lambda
* SQS queues
* HTTP/S endpoints
* AWS Event Fork Pipelines

notifications can go to Apple, Google, Fire OS, Windows devices, Android devices, ...

can fan out messages to a large number of subscribers => one same message sent to multiple different services/endpoints

SNS coordinates and manages the sending and delivery of messages to specific endpoints

We are able to use SNS to receive notifications when events occur in our AWS environment

SNS is integrated into many AWS services so it is very easy to setup notifications based on events that occur in those services (EC2, S3, IAM, CloudTrail, CloudWatch, ...)

With CloudWatch and SNS, a full environment monitoring solution can be created that notifies administrators of alerts, capacity issues, downtime, changes in the environment, ...

This service can also be used for publishing IOS/Android app notifications and creating automation based off of notifications

Benefits:

* scalable and highly reliable
* Usable through AWS console, APIs, CLI and multiple SDKs
* instantaneous push based delivery (no polling), real time events
* multiple transport protocols

Common pattern: SNS publish messages to SQS queues to reliably send messages to one or many system components async

Amazon MQ should be considered only if we have an existing app that we migrate to the cloud otherwise SNS/SQS are probably better

A topic name can be reused 30-60 seconds after being deleted => depends on the number of subscriptions

Notification cannot contain more than one message

It is possible to have duplicate message for subscribers but normally, it should only be one notification received

Notification order should be respected most of the time but it is possible that it is not the case

A message cannot be deleted once it is published to a topic

It is possible to use an SNS Delivery Policy with retry algorithm (linear, geometric, exponential backoff), maximum/minimum retry delays in case of failure.
If it is critical that all published messages be successfully processed, developers should have notifications delivered to an SQS queue (in addition to notifications over other transports).
If SNS cannot send a message to a topic, it is automatically retried (different for each service) but after 23 days, the message is discarded.

SMS can be marked as transactional for really important stuff and not promotional (=> ban in certain countries)

Can send raw message (default is JSON delivered with metadata) with "RawMessageDelivery" property on the subscriptions

SNS can be standard or FIFO

## Components

**Topic**: 

* group of subscriptions that we send a message to
* require unique names (within AWS account) limited to 256 characters => ARN with service name, region, AWS ID and topic name
* names allow alphanumeric characters plus hyphens and underscores
* topics and messages are stored redundantly across multiple servers and data centers
* policies to say who can publish message and who can subscribe to notifications
* owners can configure specific transports on the topic (permissions through ACL)
* topic can deliver to multiple different transports
* multiple publishers can send data to a topic

**Subscribers**: 

* an endpoint that a message is sent to
* available endpoints include
  * HTTP/HTTPS: POST method
  * Email, Email/JSON: need to accept email subscription first (PendingConfirmation)
  * SQS: FIFO queues not supported, queue must be created beforehand
  * Application, Mobile app notifications (iOS, Android, Amazon, Microsoft)
  * Lambda
  * SMS: phone numbers as text message
  * Kinesis Data Firehose
* can have several different subscriptions to a particular topic
* can specify the transport and not receive the same notification from multiple endpoints

**Publishers**: 

* the entity that triggers the sending of the message
  * AWS CLI
  * AWS SDKs
  * AWS services like S3 events, CloudWatch alarms, Lambda to publish to SNS, ...

## Resource Policies

* also known as SNS Access Control Policies
* grant access to a SNS topic to another AWS account
  * SNS API: AddPermission (=> can also be added with the console)
    * topic, AWS account ID(s), actions, label
    * automatically generate an access control policy to SNS
* grant access to **some** AWS services to publish to a SNS topic (many services like EC2 or Lambda will use an IAM Role instead)
* can use IAM policies and Access Control Policies at the same time

On topic -> action -> Edit topic policy

* who can publish messages to this topic (me, everyone, only these AWS users)
* who can subscribe to this topic (me, everyone, only these AWS users, only users with endpoints that match "@example.com" using these delivery protocols: HTTP, HTTPS, ...)

We can also edit the policy in the advanced view and copy/paste a JSON.

**=> We can allow a S3 notification to push notification to a topic -> S3 bucket -> events (ObjectCreate, Put, Post, Copy, Delete etc), prefix/postfix of the key, send to SNS topic**. For this the policy should have a condition like 

```json
"Condition": {
    "ArnLike": {
        "aws:SourceArn": "arn:aws:s3:*:*bucket*"
    }
}
```

then "bucket" can use events to send notifications to this topic

## Message data

* Typically JSON formatted key-value pairs
* allows developers to grab message data and parse it
* POSTs to HTTP/S endpoints with specific headers: headers allow verification of message authenticity
* message content depends on subscriber: SMS vs Lambda vs Email, ...

### Message body

* Message: message value specified when the notification was published
* MessageId: UUID, same ID must be reused for retries (with SDK)
* Signature: base64 encoded "SHA1withRSA" signature of the message
* SignatureVersion: version of SNS signature used
* SigningCertURL: the URL to the certificate used to sign the message
* Subject: optional subject param
* Timestamp: the GMT time when the notification was published
* TopicArn
* Type: type of message (Notifications are type Notification)
* UnsubscribeURL: to unsubscribe from the SNS topic

**=> the only thing we can set is the Message and the Subject, the rest comes from SNS**

We can use the JSON message generator tool which will format a JSON to a good presentation for a list of selected type of message (Email, SQS, HTTPS, ...) or target platforms (Android, iOS, ...)

This generates something like

```json
{
    "default": "Hello to all services!",
    "email": "Hello to email",
    "lambda": "Hello to lambda",
}
```

if we only selected email or lambda, we can configure the message for a particular subscriber type.

### Message attributes

* Useful for SQS and mobile push notifications
* sent along with the message
* each message attribute needs a Name, Type and Value
  * for example: "Sender" -> "String" -> "me"

=> will be found in the message in "**MessageAttributes**"

## Mobile push with SNS

Ability to send notifications directly to apps on mobile devices

Notifications sent to these endpoints can appear as message alerts, badge updates and sound alerts

Different providers allow us to send notifications to different devices:

* Amazon Device Messaging (ADM)
* Apple Push Notification Service (APNS)
* Baidu Cloud Push
* Google Cloud Messaging for Android
* Microsoft Push Notification Service for Windows Phone
* Windows Push Notification Services

Mobile Push Notification Services (MPNS) process: SNS requires "device tokens" or "registration IDs" depending on the platform to send messages to devices

**=> this is not a SMS, this is a push message on the device itself**

**=> We need to create an application in SNS and provide some info given by the providers like a push certification type and so on that allows us to do that. AWS just handles everything else for us.**

Each token can be subscribed to an unlimited number of SNS topics.

SNS default TTL for all mobile platforms is 4 weeks.

## SNS API Actions and errors

Common actions:

* create topic: just need the name
* publish: message is required
* subscribe: send endpoint a confirmation message. The endpoint owner must call "ConfirmSubscription" action with the token from the confirmation message (only valid for 3 days)
* unsubscribe: only the owner of the subscription or the topic's owner can unsubscribe, the AWS signature is required
* ListSubscriptionsByTopic / ListSubscriptions
* SetTopicAttributes: change subject and so on

Common SNS errors:

* IncompleteSignature
* InvalidAction
* InvalidParameterValue
* InvalidParameterCombination

## Monitoring

SNS sends data to CloudWatch every 5 minutes; detailed monitoring not supported

## Security

All API calls made to SNS will validate authenticity by requiring that requests be signed with the secret key of the AWS ID account and verifying the signature included in the requests.

Amazon requires an explicit op-in from subscriber to prevent spam (subscription token valid 3 days).

Amazon signs notification with private-public key pair based on certificates. Public certificate can be retrieved to validate the notification

SSL should be used for both publishers (connect to SNS over HTTPS) and subscribers (SSL enabled endpoint)

## SNS & Lambda

can invoke functions based on notification in a topic -> different lambda can be invoked for a same message

Lambda functions must belong to the same account than the topic

can subscribe lambda function to any SNS topic in any region

## Limits and restrictions

10 millions subscriptions per topic

100k topics per account

message has 256kb limit, billed as 64kb chunk so a message with 256KB payload is billed as 4 requests

140 bytes for SMS => more means more SMS sent

## Resources

CLI: https://docs.aws.amazon.com/cli/latest/reference/sns/index.html

Documentation:  https://docs.aws.amazon.com/sns/latest/dg/welcome.html

API: https://docs.aws.amazon.com/sns/latest/api/Welcome.html
