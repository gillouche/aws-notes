# AWS CLI / SDK

## General Info

Amazon Linux has the SDK installed by default but the credentials must be set.
We first should create a new user (IAM) with some permissions (Administrator or less perms). We then get an Access Key ID and a Secret Access Key for this user.
This is only for a developer access. We do not want to store credentials in an EC2 instance.
We then need to create a role that defines the permissions of the EC2 instance.

The **provider chain** is the configuration orders for the AWS CLI.

1. Environment variables
2. AWS credentials file
3. CLI configuration file
4. Container Credentials
5. Instance profile credentials (from role)

We can have MFA on API calls

## Commands

List of important commands with the CLI.

When executing commands, no reply is good reply (HTTP 200). If the command returns an error, it will be printed in the terminal.

### Generic

https://docs.aws.amazon.com/cli/latest/reference/configure/

**aws configure**: configure the credentials, only needed for a developer computer for instance, not an EC2 instance. Need the AWS Access Key ID, the AWS secret access key, the default region, the default output format (optional).

### S3

https://docs.aws.amazon.com/cli/latest/reference/s3/

**aws s3 ls**: list buckets

**aws s3 ls s3://bucketname**: list content of bucketname

**aws s3 cp source destination**: copy a local file to a bucket, destination is the bucket like s3://mybucket

**aws s3 mb s3://bucketname**: create a bucket

**aws s3 rb s3://bucketname**: remove bucket

**aws s3 mv**: move objects in the bucket

**aws s3 rm**: remove objects in the bucket

**aws s3 presign s3://bucketname/file.txt** --expires-in 300: create a presigned URL for this file (bucket private by default), valid for 300 seconds

**aws s3 sync**: sync between 2 locations (local directory to folder in a bucket)

**aws s3 website**: configures website hosting on a bucket

- \[\--index-document\]
- \[--error-document\]

S3 APIs has lower level actions like

**head-object**: returns metadata for objects without pulling the objects

**head-bucket**: returns metadata for bucket without pulling the objects

**get/put bucket-versioning**: view and modify the versioning state of the bucket, versioning cannot be disabled, only suspended

**get/put bucket-acl**: view/change access control lists on the bucket

**put-bucket-notification-configuration**: control workflows associated with update/create/delete of objects in the bucket (SNS events or lambda)

### IAM

https://docs.aws.amazon.com/cli/latest/reference/iam/index.html

**aws iam create-virtual-mfa-device** 

* --virtual-mfa-device-name username 
* --outfile /home/user/QRCode.png 
* --bootstrap-method QRCodePNG: output the QR code in a local directory for the user "username", we can upload this image on S3 (make it public) and display it on our screen for the authenticator

**aws iam enable-mfa-device** 

* --user-name username 
* --serial-number arn:aws:iam::account id:mfa/username 
* --authentication-code-1 "CODE1HERE" 
* --authentication-code-2 "CODE2HERE": the account id in the ARN is returned in the JSON from the create-virtual-mfa-device command, CODE1HERE and CODE2HERE are the two codes returned from google authenticator after putting the QR code in the authenticator

**aws iam create-role** => returns "Arn" 

* --role-name
* --assume-role-policy-document: a JSON file policy to be used with assume role

**aws iam put-role-policy**

* --role-name: an existing role name
* --policy-name: the new policy name
* --policy-document: a permissions file JSON that described the Allow effect on resources ARN (file://~/resources/Permissions.json)

### Security token service (STS)

https://docs.aws.amazon.com/cli/latest/reference/sts/index.html

**CLI can be configured to perform automatically role shifting using a base account the role ARN.**

**aws sts get-session-token**: get a MFA session from the CLI for like EC2 stop instances that require it

* --serial-number arn-of-the-mfa-device 
* --token-code code-from-token

**aws sts assume-role** => returns a set of temporary credentials for that role (general used for cross account access)

**aws sts assume-role-with-saml**

**aws sts assume-role-with-web-identity**

### OpsWorks

https://docs.aws.amazon.com/cli/latest/reference/opsworks/index.html

**aws opsworks --region us-east-1 create-deployment** 

- --stack-id
- --app-id: command dependent
- --instance-ids: command dependent
- --comment: user defined comment string
- --custom-json: json that can be referenced by recipes
- --generate-cli-skeleton: output a JSON that can be changed by the operator and given to the --cli-input-json
- --cli-input-json: accepts a skeleton (scripted use of the create-deployment command)
- --command: the command to execute. This can be **install_dependencies, update_dependencies, update_custom_cookbooks, execute_recipes, configure, setup, deploy, rollback, start, stop, restart, undeploy**

### CloudWatch

https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/index.html

Before executing these commands, we need to export our region:

export AWS_DEFAULT_REGION=us-west-2

**aws cloudwatch put-metric-alarm** => create a new alarm and associate it with a metric

* --alarm-name
* --alarm-description
* --metric-name: CPUUtilization
* --namespace: like AWS/EC2
* --statistic: Average, Minimum, ...
* --period: in seconds, should be between 10 seconds and the number of seconds in a day
* --threshold: number like 80
* --comparison-operator: stuff like GreaterThanOrEqualToThreshold, ...
* --evaluation-periods: the number of times it has to failed the comparison
* --alarm-actions: a SNS topic for example, a scale out/in policy for an ASG
* --dimensions: in the form of "Name=AutoScalingGroupName,Value=my-asg" => **in this example, the 80% threshold will be for the whole autoscaling group and not a single EC2 instance**

**aws cloudwatch put-metric-data** => publish data points, most commonly used with custom metrics such as memory used and memory free

* --namespace

**aws cloudwatch set-alarm-state** => manually change the state of an alarm, useful for testing

* --alarm-name
* --state-value: OK, ALARM, INSUFFICIENT_DATA
* --state-reason: reason of the change in JSON format

**aws cloudwatch disable-alarm-actions** => disable actions for the specific alarm, useful to disable autoscaling alarm to run some tests or investigate a problem. **The state will still change but the associated action will NOT trigger.**

* --alarm-name

**aws cloudwatch enable-alarm-actions** => enable actions for the specific alarm

* --alarm-name

**aws cloudwatch describe-alarms** => retrieve the specified alarms or all alarms if none specified

* --alarm-names: optional, format: "str1" "str2"

**aws cloudwatch get-metric-statistics** => list available metrics within the account 

* --namespace
* --metric-name
* --start-time
* --end-time
* --period

### Auto scaling

https://docs.aws.amazon.com/cli/latest/reference/autoscaling/index.html

**aws autoscaling describe-launch-configurations**

* \[--launch-configuration-names\]

**aws autoscaling describe-auto-scaling-groups**

* \[--launch-configuration-names\]

**aws autoscaling create-launch-configuration** => create launch configuration that can be used to conf ASG => this does not create an ASG

* --launch-configuration-name
* --image-id: AMI id
* --instance-type: m1.medium, ...

**aws autoscaling delete-launch-configuration**

* --launch-configuration-name

**aws autoscaling create-auto-scaling-group** => create ASG based on launch-configuration

* --auto-scaling-group-name 
* --launch-configuration-name
* --max-size
* --min-size
* --availability-zones: list of strings like "us-east-1a" "us-east-1b"

**aws autoscaling delete-auto-scaling-group**

* --auto-scaling-group-name

**aws autoscaling update-auto-scaling-group** => can modify almost all the values associated to an ASG, they are all optional

* --auto-scaling-group-name 

**aws autoscaling put-scaling-policy** => create a scaling policy, returns the ARN of the policy

* --policy-name
* --auto-scaling-group-name
* --policy-type: SimpleScaling (default), StepScaling, TargetTrackingScaling
* --scaling-adjustment: the amount by which to scale based on the specific adjustment type. Positive values add to the current capacity, negative values remove.
* --adjustment-type: (param valid only for SimpleScaling and StepScaling) ChangeInCapacity, ExactCapacity and PercentChangeInCapacityµ

**aws autoscaling put-lifecycle-hook** => update or create a lifecycle hook, for example create a notification or run a lambda function when instances are created or terminated

* --lifecycle-hook-name
* --auto-scaling-group-name
* \[--heartbeat-timeout\]: default value is 3600 seconds, min is 30 seconds, max is 7200 seconds

**aws autoscaling complete-lifecycle-action** => send a notification to the lifecycle hook

- --lifecycle-hook-name
- --auto-scaling-group-name
- --lifecycle-action-result: CONTINUE or ABANDON

**aws autoscaling record-lifecycle-action-heartbeat** => add more time to the timeout

* --lifecycle-hook-name
* --auto-scaling-group-name

**aws autoscaling enter-standby** => move instances from ASG to standby mode, good for maintenance

* \[--instance-ids\]: list of strings whitespace separated

* --auto-scaling-group-name
* --should-decrement-desired-capacity | --no-should-decrement-desired-capacity

**aws autoscaling exit-standby** => move instances from ASG out of the standby mode, good for maintenance

* [--instance-ids\]: list of strings whitespace separated
* --auto-scaling-group-name

**aws autoscaling put-scaling-policy** => creates or updates policy for ASG.

* --auto-scaling-group-name
* --policy-name

### Kinesis

https://docs.aws.amazon.com/cli/latest/reference/kinesis/index.html

**aws kinesis create-stream**

* --stream-name
* --shard-count: number of shards that the streams will use (more shared = more provisioned throughput)

**aws kinesis describe-stream** => returns RetentionPeriodHours, StreamStatus, StreamARN, StreamName, Shards (list)

* --stream-name

**aws kinesis get-shard-iterator** => returns "ShardIterator" with the value to be used with **get-records**

* --stream-name
* --shard-id
* --shard-iterator-type: shard iterator behavior
  * AT_SEQUENCE_NUMBER: start read at position provided in the value
  * AFTER_SEQUENCE_NUMBER: start reading after position provided in the value StartingSequenceNumber
  * AT_TIMESTAMP: position denoted by the value of "Timestamp"
  * TRIM_HORIZON: read at the last untrimmed record in the shard (the oldest)
  * LATEST: after the most recent record in the shard

**aws kinesis get-records** => returns "Data" which is base64 encoded

* --limit: number of records to retrieve
* --shard-iterator: the shard iterator returned from **get-shard-iterator**

### Logs

https://docs.aws.amazon.com/cli/latest/reference/logs/index.html

**aws logs put-subscription-filter** => create subscription filters for real time log processing

* --log-group-name: an existing log group name
* --filter-name: an existing filter name (for update) or a new one if none exist, **cannot have 2 filters on a same log group**
* --filter-pattern
* --destination-arn: an existing kinesis stream ARN to send matching log event
* --role-arn: an existing role ARN with valid policies (CW logs perm to deliver to destination stream)

### RDS

https://docs.aws.amazon.com/cli/latest/reference/rds/

**aws rds describe-db-instances** => get info on instances

### DynamoDB

https://docs.aws.amazon.com/cli/latest/reference/dynamodb/

**aws dynamodb get-item** => default eventually consistent read, can be changed in the param

**aws dynamodb batch-get-item** => use primary keys to retrieve multiple items from one or multiple tables

**aws dynamodb query** => one or more items from a table or a secondary index 

**aws dynamodb scan** => get every items in the table, eventually consistent

**aws dynamodb put-item** => replace/create

**aws dynamodb update-item** => modifies the attributes of an existing item

**aws dynamodb delete-item** => delete by primary key

**aws dynamodb batch-write-item** => multiple put/delete requests across multiple tables 

**aws dynamodb create-table** => with defined throughput settings

**aws dynamodb update-table** => change throughput settings

### EC2

https://docs.aws.amazon.com/cli/latest/reference/ec2/

**aws ec2 run-instances** => **create instances**

**aws ec2 stop-instances** => stop instances, cannot be used on spot instances

**aws ec2 start-instance** => start instances when they are in stopped state

**aws ec2 terminate-instances** => terminate instances and delete EBS which have the delete on termination flag. EBS volume attached to the instances after it has started have this flag set to false and will remain after the termination

**aws ec2 describe-instances** => get info from one or more instances

**aws ec2 wait** => holds until a particular condition is satisfied (instance running, snapshot complete, ...)

**aws ec2 create-image** => creates EBS backed image AMI from running or stopped instances => contains all the volumes attached at the time of creation but not the ones added after the instance started.

**aws ec2 describe-snapshots**

* --owner-ids 
* --filters: Name=status,Value=pending

**aws ec2 create-snapshot** => encrypted ebs also have encrypted snapshots, restoring from encrypted snapshots created an encrypted ebs

**aws ec2 delete-snapshot**

**aws ec2 copy-image** => from region to region

**aws ec2 copy-snapshot** => encrypted snaps remained encrypted in the destination region

**aws ec2 create-volume** => create new EBS volume

* --availability-zones (mandatory), the rest is optional
* --encrypted
* --iops
* --kms-key-id
* --size
* --snapshot-id
* --volume-type

**aws ec2 describe-tags** => list tags in our environment (backup, pruning, ...)

### SQS

https://docs.aws.amazon.com/cli/latest/reference/sqs/

**aws sqs add-permission** => add other entities access to our queues

**aws sqs change-message-visibility** => visibility timeout of a specified message in a queue to a new value

**aws sqs set-queue-attributes** => can take up to 60 secondes to propagate in all the queues. Change of retention period can take up to 15 minutes

**aws sqs send-message, receive-message, delete-message**

### Lambda

https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html

**aws lambda add-permission** => resource based policy like DynamoDB Streams to push to AWS lambda, S3, ... they need permissions to do that

* --function-name
* --statement-id
* --action
* --principal

**aws lambda create-event-source-mapping** => creates a mapping between an event source (Kinesis Stream and DynamoDB streams) and an AWS Lambda function. Lambda reads items from the event source and triggers the function => only valid with streams of data. We don't need the same permissions than "add-permission" for streams.

* --event-source-arn
* --function-name

**aws lambda create-function** => can create a function from a zip (in the body) or a S3 bucket referenced

* --function-name
* --runtime
* --role
* --handler: filename.function_name
* --code: zip file or S3 bucket / --zip-file fileb://function.zip to upload directly

**aws lambda invoke**

* --function-name
* [--invocation-type]: RequestResponse (default, synchronous), Event (async), DryRun

