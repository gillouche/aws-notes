# Amazon Inspector

## General Info

* Tools really oriented towards security and not to improve billing like Trusted Advisor. 
* Do network and host analysis of EC2 instances 
* Automated security assessment service that helps improve security and compliance of applications deployed on AWS. 
* Auto assess for vulnerabilities or deviations from best practices. 
* Produce a detailed list of security findings prioritized by level of severity. Can be reviewed directly or as part of detailed assessment reports which are available via the Amazon Inspector Console or API.
* runs assessment that check for security exposures and vulnerabilities in EC2 instances
* can be configured to run on a schedule
* need an agent installed on EC2 for host assessments
* for network assessments, we do not require an agent -> for some checks only

Network assessments:
* network config analysis to check for ports reachable from outside the VPC
* if the inspector agent is installed on the EC2 instances, the assessment also finds processes reachable on port
* price based on the number of instances assessments

Host assessments:
* vulnerable software (CVE), host hardening (CIS benchmarks), and security best practices
* requires an agent (auto-install with SSM Run Command)
* price based on the number of instance assessments

Requirements:

* Inspector needs TAGS to work
* Inspector needs a role with ec2:DescribeInstances, can be created with Inspector
* Inspector needs an agent running on EC2 instances -> **SSM role to be able to install the agent (via run command)**

Allows for:

* analyzing the behavior of our AWS resources (Windows or Linux)
* identifying potential security issues

Features:

* configuration scanning and activity monitoring engine:
  * determines what a target looks like, its behavior and any dependencies it may have 
  * identifies security and compliance issues
* built in content library:
  * rules and reports built into inspector
  * best practice, common compliance standard and vulnerabilities evaluations (CVE, not AWS specific)
* detailed recommendations for resolving issues
  * API automation
  * allows for security testing to be included in the development and design stages

AWS does not guarantee that following the provided recommendations will resolve every potential security issue

**We can download an assessment report of the findings (several hundreds pages). This is either the finding report or the full report; HTML or PDF format.**

**=> Inspector is a security tools that allows us to evaluate how the configuration, settings, packages and security footprint of EC2 instances match against the risk rules. This is different than AWS Config. => use Inspect if we need a report on advanced security inspection**

**Inspector is not a point in time, the analysis takes some time to be complete. Config only analyzes configuration properties and Systems Manager only deals with packages. Inspectors is the service to use for real security analysis.**

Use AWS Lambda to write automatic approval rules. Store the approved AMI list in AWS Systems Manager Parameter Store.
Use Amazon EventBridge to trigger an AWS Systems Manager Automation document on all EC2 instances very X days (compliance). 
Inspector will scan for CVE assessment on the approved AMI via the EC2.

## Concepts

**Target**: a collection of one or more EC2 instances, **can select them all or use tags!** We can preview the targets (EC2 detected) and we can install the agent with run command if it is not already there. The agent is "**HEALTHY**" when it successfully installed, otherwise it is "UNKNOWN".

**Assessment** **template** made up of

* security rules (= a check for a potential security issue)
* targets: defines what (EC2 instances; all or tags) 
* package rules 
* duration (more time gives more results, default is one hour) 
* We can define SNS topics for notifications.
* can specify recurring assessment like runs once every 7 days with the first run starting now
* **=> produce a list of findings**

**Assessment run**: applying the assessment template to a target

**Findings**:

* HIGH
* MEDIUM
* LOW
* Informational

## Rules packages in Inspector

* common vulnerabilities and exposures (CVE) like OWASP
* center for internet security (CIS) benchmarks
* security best practices: disable root over SSH, SSH version 2 only, password policy, ...
* runtime behavior analysis: insecure client protocols, unused listening TCP ports, root process with insecure permissions

**Not all packages are supported on all OS!** Good practice is to apply them all whenever possible.

## Working steps

1. Create assessment target (based on EC2 tags)
2. Install agents on EC2 instances
3. Create assessment template: select rules packages (Security best practice, Runtime Behavior Analysis, ...) -> can select them all if wanted, select the duration (1 hour recommended)
4. Perform assessment run
5. Review findings against rules: huge reports (several hundred pages), severity level (High, medium, low, informational)

## Actions

**Will do**:

* monitor network, file system, process activity within the specified target
* compare what it sees to security rules
* report on security issues observed within target during run
* report findings and advise remediation

**Will not do**:

* relive us of our responsabilities under the shared responsability model (need to patch EC2 ourselves for instance)
* perform miracles 

## Notifications

We can either get notified directly from Inspector (assessment template) or we could select an event source in CloudWatch

**With CloudWatch, it is possible to create automatic remediation for any of the findings generated by Inspector.**

## Billing

Cheap if we don't have many instances to analyze: $0.15 per instance assessment

First 250 instance assessments for the first 3 months are free
