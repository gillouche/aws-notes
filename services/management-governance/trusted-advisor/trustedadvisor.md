# Trusted Advisor

## General Info
Check for problems on our account and notify us, core checks and recommendations, provides best practices for

- Cost Optimization
- Performance
- Security: basic check like MFA enabled, security groups unlocked, ... -> not advanced checks like Inspector at EC2 level
- Fault tolerance
- Service Limits: warning when we reach 80% of service limits (need to call AWS for more)
- things running idle or not being used -> go through them and turn them off, counts external API calls for services that charge per request
- helps customers provision resources

**Need a business/entreprise account for most advanced checks (business/entreprise level support).**

Trusted advisor checks:

* Amazon EC2 reserved instances optimization
* low utilization Amazon EC2 instances
* idle load balancers
* Underutilized Amazon EBS volumes
* Unassociated Elastic IP Addresses
* Amazon RDS idle db instances
* Amazon Route 53 latency resource record sets
* Amazon EC2 reserved instance lease expiration
* Underutilized Amazon Redshift clusters

Trusted Advisor Dashboard:

* weekly email notifications of updated alerts
* overview of the cloud configuration (cost optimization, performance, security, fault tolerance)
* list of recent changed alerts (cloud trail logging, security groups unrestricted, ...)
* new features updates (checks, features)

Use case:

* monitor service limits, security groups (specific ports unrestricted), IAM use
* consider separate accounts for production and non production
* limit visibility: different permissions, consider using roles, separate capacity limits

Lambda can retrieve the most current utilization and service limit data and send notifications 

## Monitoring

can use CloudWatch events to detect and react to changes in the status of Trusted Advisor checks. Then based on the rules we create, CloudWatch Events invokes one or more target actions when a check status changes to the value we specified in the rule.

Can select the following types of targets when using CloudWatch events:

* AWS lambda functions
* Amazon Kinesis Streams
* Amazon SQS
* built-in targets (CloudWatch alarm actions)
* Amazon SNS
