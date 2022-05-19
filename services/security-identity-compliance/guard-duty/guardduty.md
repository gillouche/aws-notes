# Amazon GuardDuty

## General Info

Intelligently monitors event sources (VPC Flow Logs, Route 53 DNS query logs, CloudTrail events, other threat intelligence)

ingests other feels such as known attacks, malicious IPs and domains and utilizes machine learning techniques to identify anything expected and potentially authorized in AWS accounts such as unexpected infrastructure deployments in a previous unused region or unusual API calls

Guard Duty makes its findings visible via the Guard Duty console or it can generate CloudWatch events allowing notification or automated remediation

GuardDuty doesn't manage AWS CloudTrail logs, VPC Flow Logs and so on or make their events and logs available to us. We can configure the settings of these data sources through their respective consoles or APIs. We can suspend or disable GuardDuty at any time to stop it from processing and analyzing events and logs.

GuardDuty can scans multiple accounts together, there is an account that is designated as the master GuardDuty account (=> it must invite all the other accounts), the others are member accounts. **The GuardDuty account is not necessarily the same as the AWS Organizations master account. For a security perspective, it is better to differentiate them.** A member can only be linked to a single master GuardDuty account.

There is the concept of **trusted IP list** where GuardDuty does not take them into consideration when generating findings. There is also **threat list** where can define a list of known malicious IP addresses. Can have 6 threat lists per region per account but the trusted IP list is limited to the member account.

**GuardDuty is fast but not real time (CloudWatch events)!**

* intelligent threat detection service
* detects account compromise, instance compromise, malicious reconnaissance and bucket compromise
* continuous monitoring for events across:
  * CloudTrail Management & S3 Data events
  * VPC flow logs
  * DNS logs
  * 

## Billing

per 1 million events

per GB of VPC Flow Logs and DNS logs analyzed

can become expensive if we have lots of events
