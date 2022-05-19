# General Information about AWS

## Terminology
* RTO (recovery time objective): how quickly we need to have everything back on in case of issue
  * read replica in another region that can be promoted to standalone DB cluster if needed
  * hot standby of application tiers in another region
* RPO (recovery point objective): maximum amount of data, as measured in time, that can be lost after a recovery from disaster 
* TCO (total cost of ownership): know how much your resources cost (on prem servers, AWS, ...)
* CART (AWS Cloud Adoption Readiness Tool): helps organizations of all sizes develop efficient and effective plans for
cloud adoption and enterprise cloud migrations => 16 questions online survey about business, people, process, platform, operations and security
* RBAC (role based access control)
* LOB (line of business application): very important app

## Architecting a system
* know the read/write patterns
  * stable traffic vs unpredictable
  * write problems to DB
    * use a queue in front of the writing application (Lambda, ...)
  * read problems from DB
    * caching or read replica
    * DAX for DynamoDB
  * caching
    * can we live with not up-to-date data returned or not?
    * we can only cache read requests
* know RTO, RPO
  * the shorter the RPO is, the more costly it will be => DB replicas in other regions, scaled down production in the other regions
* required response time
* scaling
  * slow scaling needs: EC2 with ASG is fine
  * medium: ECS
  * big scaling needs: need serverless (SQS, Lambda, ...)
    * if processing takes more than 15 minutes, no Lambda (hard timeout limit)
  * for SQS scaling, use ApproximateNumberOfMessages queue attribute metrics
* resources organizations
  * need tag -> use Tag Editor to update tags of multiple resources at the same time
* pilot light
  * replicate part of the IT structure for a limited set of core services
  * small part always running simultaneously syncing mutable data (db or docs) while other parts of the infra are switched of
* backup/restore approach
  * must ensure that most critical core elements are already configured and running in AWS
* if highly available -> need multiple AZ

## Free tier

Lots of services fall into the free tier category (the main usage is covered).
What's not covered: 

- AWS PIOPS volume of 10GB size

## AWS default limits

https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html

## API access

AWS Console login/passwords 
Signing Certificates
Access Keys (for the API) -> not for EC2, only the API
Key Pairs -> only access to EC2, not the API

## Pricing
* 3 primary prices
  * compute: amount of resources (CPU, RAM, duration)
  * storage: quantity of data stored
  * outbound data transfer: quantity of data that is transferred out from all services (internet or regions)
* 3 types of paying structure
  * pay-as-you-go: no commitment; pure pay-as-you-go with no contracts or termination fees
  * save when we reserve: reserve capacity for 1 or 3 years for a substantial discount
  * pay less by using more: some pricing is tiered, if we use more we pay less per unit

Good to know for exams
* which is more expensive: ElastiCache or an RDS read replica? Read replica is cheaper
* what's the most cost-effective block storage for 3000 IOPS? (do we need provisioned or not based on the IOPS requirements?)
* which data transfer is charged vs not charged (inbound, outbound, inter region, inter AZ)
* [AWS Pricing Calculator](https://calculator.aws/#/) or the individual services pricing pages

### Cost allocation tags
* easier to find what costs money in our account with the tags (environment, app name, department, ...)
* user defined cost allocation tags: Environment, Name, ... whatever we define in the tags
* AWS generated cost allocation tags

With tags, we can then use AWS cost explorer to filter

### Cost and usage reports
In the Billing section, we can generate a report at a certain time frequency to an S3 bucket

Much more detailed than normal billing info

## Security and Compliance

Best way to handle audit: create a new Auditors group in IAM, apply read only policy to auditors with full read access, create user accounts for the auditors
We cannot have the same login ID for different user (with different password)

Best practice:

- request and obtain applicable third party audited AWS compliance reports and certifications
- Gather evidence of IT operational controls
- Request and obtain approval from AWS to perform relevant network scans and in-depth pen test of our system

**AWS Compliance frameworks (most important)**: PCI security standards council, ISO, HIPAA (health compliance US)

**DDOS**: https://d1.awsstatic.com/whitepapers/Security/DDoS_White_Paper.pdf
Technologies that can be used to mitigate DDoS: CloudFront-Route 53-ELB (all three are protected by AWS Shield), WAFs (layer 7 attacks), Autoscaling (use for both WAFs and Web Servers), CloudWatch

**AWS Shield**: turned on by default, $3k a month if we want advanced option (incident response team and in depth reporting), customer doesn't pay if victim of an attack

**AWS Market place**
can purchase security products from third party vendors on the AWS market place
Firewalls, hardened OS's, WAF's, Antivirus, Security Monitoring, ...
Free, hourly, monthly, annual, BYOL
Center of Information Security (CIS) OS hardening
Subscriptions like A cloud Guru

**IAM**
can create custom policies using visual editor or JSON
can attach roles to EC2 instances at any time using the command line or AWS console
once attached, the roles takes effect almost immediately 
any policy change also takes effect almost immediately
IAM:PassRole -> passing a role to an AWS service to assign temporary permissions to the service, passing a role to another AWS account

**MFA reporting & IAM**
can enable MFA using command line or the AWS console
MFA can be enabled on both root account and user accounts
can enforce the use of MFA with the CLI by using the STS (security token service), can enforce the use of MFA using IAM
can generate credential reports (IAM) to know which user is using MFA or not (+ other infos)

**Security Token Services**
Employees uses login/pw of LDAP/facebook/... to a web application
App talks to Identity broker service (manually created)
Identity broker service logs in with credentials to LDAP/facebook/... and receive a token
If token valid, Broker Service get a new token from AWS STS (duration, services permissions, ...)
Token from STS used by Web application to connect to AWS services
AWS services check STS token against IAM

=> STS gives temporary access using methods: Federation with Web Identity Providers (**AssumeRoleWithWebIdentity**), Cross Account Access, Active Directory Federation (**AssumeRoleWithSAML**)
=> Active Directory Federation Services is an identity broker that can be used to enable Active Directory accounts to access AWS resources
=> Web Identity Federation with Cognito is the way to go for mobile apps and temporary security credentials (**AssumeRoleWithWebIdentity**)

**Logging in AWS**
CloudTrail: API calls (stored in S3)
Config: config changes + notification
CLoudWatch logs: performance logs
VPC Flow logs: network logs between VPC

**AWS Hypervisors**
HPM over PV where possible
PV is isolated by layers (Guest OS sits on layer 1, Application Layer on layer 3)
Only AWS admins have access to hypervisors
AWS staff do not have access to EC2 -> customer's responsability
All storage and memory is scrubbed before it is used by another customer

**Dedicated instances vs Dedicated Hosts**
Both have dedicated hardware
Instances are charged by the instance, hosts are charged by the host
If specific regulatory requirements or licensing conditions -> dedicated hosts
Instances may share the same hardware with other AWS instances from same account that are not dedicated
Hosts give much better visibility (sockets, cores, host ID, ...)

**AWS systems manager run command**
Commands can be applied to a group of systems based on AWS instance tags or by selecting manually
SSM agent needs to be installed on all the managed instances (+ need IAM role)
Commands and parameters are defined in a Systems Manager document
Commands can be issued using AWS console, AWS CLI, AWS tools for Windows powershell, Systems Manager API or Amazon SDKs
Can use the service with on-premises systems as well as EC2 instances

**AWS systems manager parameter store**
store password, database connection strings, license codes 
store values as plain text or we can encrypt the data
can reference these values by using their names
service can be used with EC2, CloudFormation, Lambda, EC2 Run Command, etc

**Presigned URL S3**
can access objects using pre signed URLs
done via SDK but can be done with CLI
they expired, default is 1 hour
"--expires-in" followed by seconds to change it
Great way to restrict who can view objects since we can just share the presigned URL to the people we want to have access.

**AWS Config rules with S3**
No public read access
No public write access

**AWS inspector**
create assessment target (using tags)
install agent on EC2 instances (cannot do that with RDS, DynamoDB, ...)
create assessment templates: Common Vulnerabilities and exposures, CIS operating system security configuration benchmarks, Security best practices, Runtime behavior analysis
perform assessment run
review findings against rules (severity levels: high, medium, low, informational)

What does it do ?
monitor network, file system, process activity within the specified target
compare what it sees to security rules
report on security issues observed within target during run
report findings and advise remediation
=> vulnerability scanning of applications running on EC2

What does it NOT do ?
relive us of our responsability under the shared responsability model
perform miracles

**Trusted Advisor**
related to billing mostly

Cost Optimization
Availability
Performance
Security (basic security of account, different than AWS inspector

=> should be used to get insights into our AWS environment to help determine what can be improve

**Shared Responsability Model**
responsible for things like EC2 OS patching, Antivirus, Security groups, ACL, Encryption EBS, lifecycle IAM credentials, ... => anything that we can control
not responsible for things like RDS OS updates, RDS DB updates, PHP updates with Elasticbeanstalk, AWS protects against IP spoofing or packet sniffing (traditional network security issues)

**Security groups**
security group are stateful, if we open input port (ingress), the port is also open for output (egress)

Check security groups if we have suspect connections to an EC2 instances in a private subnet behind a bastion. We might have other instances that can connect using security group with 0.0.0.0/0

**CloudTrail logs**
Great to monitor the environment (API calls)
Stores logs in S3, use Athena to go through them instead of manually

**AWS Artifact**
Service where we can download documents about security and compliance on AWS that we can give to auditors or regulators.

**CloudHSM vs KMS**

CloudHSM 
Tenancy: Single
Scale & HA: HA service from AWS
Key control: Customer
Integration: Broad AWS support
Symmetry: Symmetric & Asymmetric
Compliance: FIPS 140-2 & EAL-4
Price: $$

KMS
Tenancy: Multi
Scale & HA: HA service from AWS
Key control: Customer + AWS
Integration: Broad AWS support
Symmetry: Symmetric
Compliance: good
Price: $

**Encryption**
Instant with S3
requires migration for DynamoDB, RDS, EFS, EBS
Elasticache for Redis offers native encryption but not Elasticache for Memcached

## Regions and availability zones

Each region (geographic area) has 2 or 3 availability zones (data center).
17 regions currently, nort virginia is the main one where all the services not region dependent are attached

## HA and fault tolerance

HA: the system will continue to function despite the complete failure of any component of the architecture -> app still functions if it loses a web server or node in a cluster

* use multiple AZ and other regions
* use auto scaling
* take advantages of HA services such as multi AZ RDS, S3, ELB, DynamoDB, SQS
* geographical location
  * multi AZ: customers located in same geo region
  * multi region: customers located around the world
* point of failure
  * multi AZ: single point of failure is the region
  * multi region: satisfies the most stringent COOP/DR requirements
* leveraging ELB and Route 53
  * multi AZ: with zone apex support
  * multi region: multi region latency based routing (LBR)

FT: the system will continue to function without degradation in performance despite the complete failure of any component of the architecture -> quickly spin up resources that mitigate the risk of loss in performance

* use HA services to provision enough capacity
* often involves additional compute capacity to guarantee

## Appropriate use of Multi AZ vs Multi Region architectures

RDS

* cross region snapshot copy
* cross region read replicas

EBS

* cross region snapshot copy

S3

* cross region replication

DynamoDB

* data pipeline
* streams

EC2 instances

* cross region AMI copy
* the AMI ID changes

## Scalability

Loosely Couple

* design independent architectures with independent components
* use SQS and SNS to share information between components
* ELB for two way traffic, immediate handling of requests
* Kinesis for streaming, clients read and track stream position
* ASG for scalable compute

Become stateless

* determine how to maintain app persistence and state within and between each component 
* use AWS services such as DynamoDB and elasticache to maintain state between applications

Leverage parallelism

* one server running for five hours is the same price as five servers running for one hour
* the efficacy and cost of the compute power we want to use can determine if we need to vertically scale or horizontally scale

Frontend scaling architecture

* EIPs and Route 53
  * using 3rd party load balancers
  * using TCP ports that are supported by ELB
  * using web sockets not supported by ELB
  * need direct access to the instances
  * utilize health checks in Route 53
  * use round robin DNS

middle tier scaling architecture

* ELB -> ASG
* ELB -> ASG -> ELB -> ASG where the second part is internal (not publicly accessible, separation of tiers, independent scaling)
* ELB -> ASG -> SQS queue -> ASG: asynchronous tasks, single direction only, unordered, at least once delivery
* ELB -> ASG -> 2 x SQS queue (request and response) -> ASG (need an identifier for return messages)
* ELB -> ASG -> Kinesis -> ASG: async tasks, single direction only, ordered within a shard, at least once delivery, independent stream position
* ELB -> ASG -> SNS (fan out to SQS) -> several SQS with each an ASG

Data storage scaling architecture

* static content to S3, lower overhead compared to EC2, concurrent access from multiple resources
* scale S3: GET requests, CloudFront recommended, smaller number of larger files can lower cost and increase performance
* S3 classes: standard, IA, archive
* scale EBS
  * snapshot existing volume, EBS volume from snapshots
  * add larger volume for EC2 instance, migrate using OS tools
  * for DB, holding code
  * other benefits
* scale RDS: resize on the fly, extend read replicas, async communications, direct queries to the read replicas
* elasticache: cache common requests, cache in front of relational DB, cache extends read through capabilities
* scaling DynamoDB: increase/decrease read and write capacity units, 4kb item unit size, global or local secondary indices for faster queries. Can also use elasticache for DynamoDB.

## Elasticity

* use AWS auto scaling as much as possible
* don't assume health, availability or fixed location of components
* automate everything
  * installation and configuration of environments
  * dynamic configurations

## Self healing architectures

* important to build highly available applications
* anticipate failure by monitoring
* recover from a failure that may require a server to be rebooted or relaunched
* relaunching a server
  * bootstrapping to dynamically recover the server
  * persistent state of application acquired from S3 or DynamoDB
* done fear constraints
  * need more RAM -> consider distributing load across machines or a shared cache
  * need better IOPS for DB ? instead consider read replicas, sharding or DB clustering
  * hardware failed or config got corrupted ? rip and replace
* auto scaling for stateless applications, keep the state outside the instances
* user data scripts: reattaching an EBS volume, EIP, DNS changes
* Data tier: aurora or RDS multi AZ, S3 has own data integrity checking, ElastiCache for Redis can have multiple nodes for recovery
* multi site failover
  * corporate data center - AWS
  * AWS multi region
* container failover
  * DB mirroring to RDS
  * snapshots of docker servers to S3 using storage gateway
  * if failure, just start ECS cluster 

## Cost savings best practices

* EC2 reserved instances 
  * all up front (AURI)
  * partial up front (PURI)
  * no upfront (NURI)
* EC2 spot instances
  * bid on spare Amazon EC2 computing capacity
  * batch processing, media processing, multi part data processing
  * can also use EMR with spot instances
  * can be used with Jenkins to scale up/down based on the number of jobs to be completed
* Amazon CloudWatch
* AWS trusted advisor: find unused stuff
* AWS cost explorer
* Building automation
  * trusted advisor notification to lambda and users
  * lambda deals with unused resources
* reserved instances for on-demand and the rest for spot instances with a state persistence in DynamoDB

## Tags

Tags are key value pairs attached to AWS resources (Metadata)
Can sometimes be inherited (autoscaling, cloud formation, elastic beanstalk can create other resources)
Tags don't have to be created at resources creations, we can add them later
**tags are case sensitive**

## Resources groups

Group resources based on tags, they can share one or more tags.
Resource groups are setup in all the different services that support it (EC2, CloudWatch, ...)
Groups can have tags as well but when we add a tag to a group, it doesn't tag the resources with this tag.
We can organize AWS resources according to user defined tags.
Good practice: tag everything, for a same instance -> can have same value for different key but all keys must be different, maximum tag key size is 128 unicode char

Contains info such as region, name, health checks
and specific information like 

- public & private IP addresses (EC2)
- port config (ELB)
- database engine (RDS)

Two types:

- classic resource groups: global resources (get info from all regions, all organization unit, ... if wanted)
- AWS systems manager: regional, can push an action to all instances in the same region or some other resources

An action can be applied to a group (terminate instance, ...).

## Backups

For resources like a DB on EBS that cannot be stopped, we can create a read replicas and create snapshots from this replica in order to not impact the master database.

Great services for backups: S3, Glacier, Storage Gateway to S3, EBS snapshots, RDS automated backups (auto by AWS) + snapshots (users initiated)

## Health Dashboards

Two types:

- service health dashboard: shows health of each AWS service as a whole per region https://status.aws.amazon.com/
- personal health dashboard: provides alerts and remediation guidance when AWS experiences events that may impact us

## Elasticity and scalability

- Elasticity 
  allows stretching out and retract back our infrastructure based on demand.
  We only pay what we need.
  Elasticity is used during a short time period such as hours or days.
  => **scale with demand (short term)**
- Scalability
  used to talk about building out the infrastructure to meet demands long term
  used over longer time periods such as weeks, days, months and years.
  => **scale out infrastructure (long term)**

## Encryption and downtime

For most AWS resources, encryption can only be enabled at creation (except S3).

- Elastic File System (EFS -> NFS protocol, shared between multiple EC2 instances):
  need to create a new encrypted EFS and copy data from an existing one, cannot encrypt while being used!
- RDS: if we want to encrypt an existing RDS, need to create a new encrypted database and migrate the data
- EBS: 
  encryption must be selected at creation time. 
  We cannot encrypt an unencrypted volume or unencrypt an encrypted volume. 
  We can migrate data between encrypted and unencrypted volumes (rsync or Robocopy) => EBS will handle the encryption automatically. 
  If we want to encrypt an existing volume, we can create a snapshot and apply encryption at the same time to get an encrypted snapshot. Then restore the encrypted snapshot to new encrypted volume.
- S3:
  much more flexible
  S3 buckets: can enable encryption at any time
  S3 objects: can enable encryption at any time

Apart from S3, it is good practice to stop the applications for the data migration

**=> Instant encryption (S3) / encryption with migration (DynamoDB, RDS, EFS, EBS)**

## Compliance

Amazon is compliant with a bunch of standards and recommendations.
https://aws.amazon.com/compliance/

- PCI Security Standards Council: international standards, payment card industry data security standard (PCI DSS v3.2) is widely accepted set of policies and procedures intended to optimize the security of credit, debit and cash card transactions and protect cardholders against misuse of their personal information. (**it is not because AWS is PCI DSS compliant that whatever we do with AWS is PCI DSS compliant, our application needs to be audited to be PCI DSS compliant**)
- ISO (international standards): ISO/IEC 27001:2005 specifies requirements for establishing, implementing, operating, monitoring, reviewing, maintaining and improving a documented **information security management system** within the context of the organization's overall business risks.
- HIPAA: healthcare information in the US, easier for people to keep health insurance  protect the confidentiality and security of healthcare info and help the healthcare industry control administrative costs => not all services are HIPAA compliant (take some time after general availability)
- FedRAMP (Federal Risk and Authorization Management Program): (for US companies) government wide program that provides a standardized approach to security assessment, authorization and continous monitoring for cloud products and services.
- NIST (National Institute of Standards and Technology, US Department of Commerce): standards to help organizations manage cybersecurity risks 
- SAS 70: statement on auditing standards No. 70
- SOC1: service organization controls - accounting standards
- FISM: fedora information security modernization act
- FIPS 140-2: US Government compute security standard used to approve cryptographic modules. Rated from level 1 to level 4 with 4 being the highest security. Cloud HSM meets the level 3 standard.

## DDoS

https://d0.awsstatic.com/whitepapers/Security/DDoS_White_Paper.pdf

Distributed Denial of Service (DDoS): attack that attempts to make the website or app unavailable to the end users. Achieved by multiple mechanisms such as large packet floods by using a combination of reflection and amplification techniques or by using large botnets.

### Amplification/Reflection attacks

Include things such as NTP, SSDP, DNS, Chargen, SNMP attacks.
An attacker may send a third party server (such as an NTP server) a request using a spoofed IP address (pretending to be someone else's IP). That server will then respond to that request with a greater payload than initial request (usually in the region of 28x54 times larger than the request) to the spoofed IP address.
This means that if the attacker sends a packet with a spoofed IP address of 64 bytes, the NTP server would respond with up to 3456 bytes of traffic. Attackers can co-ordinate this and use multiple NTP servers a second to send legitimate NTP traffic to the target.
=> **floods the spoofed IP address with traffic**

### Application attacks (layer 7)

Flood the web server with GET requests which cannot handle all these requests and stop accepting connections.

Slowloris attack: send as many requests that are slow to handle as possible (with headers that continue without finishing the request), the goal is to keep as many connections open as possible.

### How to mitigate DDoS ?

Minimize the attack surface area (ALB with web application firewall instead of round robin DNS).
Be ready to scale to absorb the attack (auto scaling group).
Safeguard exposed resources
Learn normal behavior and try to protect against abnormal behavior.
Create a plan for attacks.

Good AWS service to help against DDoS:

- AWS Shield (protects CloudFront, Route 53, ELB)
- WAFs
- Autoscaling (use for both WAFs and Web Servers)
- CloudWatch (for warning)

## AWS Marketplace - Security products

https://aws.amazon.com/market
provides AMI to be used in EC2 instances, trainings, databases, business intelligence, ... -> not only AMI
Marketplace is **region specific**

There is a "security" category where we can find penetration testing.
For penetration testing, we need to submit an "AWS vulnerability / penetration testing request form" to request authorization for pen test to or originating from any AWS resources. **even if we bought a pen test product on the marketplace**

**can purchase security products from third party vendors on the AWS market place: firewalls, hardened OS's, WAF's, Antivirus, Security monitoring etc**
**free, hourly, monthly, annual, BYOL, etc**
**Center of Internet security (CIS) OS Hardening: someone creates a hardened version of an image that we can buy**

## Security & Logging

https://d0.awsstatic.com/whitepapers/compliance/AWS_Security_at_Scale_Logging_in_AWS_Whitepaper.pdf

Logging in AWS can use several services:

- AWS CloudTrail: records all API calls
- AWS Config: records the state of the configuration (initial, changes, ...)
- AWS CloudWatch logs: performance metrics, ...
- VPC Flow Logs: network traffic across VPCs

**We should also control access to log files (security guys, sysadmins maybe, not developers or the rest)**

- Prevent unauthorized access (IAM users, groups, roles and policies), Amazon S3 bucket policies, Multi factor authentication
- Ensure role-based access (IAM users, groups, roles and policies), Amazon S3 bucket policies

**We should receive alerts when logs are created or fail -> CloudTrail notifications and AWS Config Rules**
Alerts should be specific but not give too much information, we should have a CloudTrail SNS notifications that only point to log file location

**We should also manage changes to AWS resources and log files**
Log changes to system components -> AWS config rules and CloudTrail
Contols exist to prevent modification to logs: IAM and S3 controls and policies, CloudTrail log file validation (check if somebody changed the logs), CloudTrail log file encryption

## AWS Hypervisors

Hypervisor or virtual machine monitor (VMM): computer software, firmware, hardware that creates and runs virtual machines. 
Host machine: computer on which a hypervisor runs one or more virtual machines. Each VM is called a guest machine

EC2 runs on Xen Hypervisors which can have guest operating systems running either as Paravirtualization (PV) or using Hardware Virtual Machine (HVM).
HVM guests are fully virtualized. The VMs on top of hypvervisors are not aware that they are sharing processing time with other VMs.

PV is a lighter form of Virtualization and it used to be quicker but now the perf gap has now closed and **Amazon now recommends using HVM over PV where possible**. 
PV guests rely on the hypervisor to provide support for operations that normally require privileged access. CPU provides 4 separate privilege modes called rings. Ring 0, most privileged (Host OS + Xen Hypervisor), guest OS runs in Ring 1 (EC2) and applications in ring 3.

Windows EC2 can only be HVM where Linux can be both PV and HVM.

### Isolation

Customers are completely isolated from each other.
The physical network interface sees all the requests but then there is a firewall at host level that redirects requests to customer specific resources (security groups, virtual interfaces, hypervisor, customer 1).

### Hypervisor access

Administrators with a business need must use MFA, actions are logged and audited. When the job is done, the access to the relevant hosts is revoked.

### Guest (EC2) access

Virtual instances are completely controlled by the customer. Full root access or administrative control over accounts, services and applications. **AWS does not have any access rights to the instances or the guest OS**.

### Memory Scrubbing

EBS blocks are automatically reset between customers.
Memory is set to 0 by the hypervisor when it is unallocated to a guest.
The memory is not returned to the free memory pool until the memory scrubbing is complete.

## Shared responsability model

Amazon manages security _of_ the cloud (house, landlord manages fences, fire alarms, ...), customer manages security _in_ the cloud (house, tenant manages security of the objects in the house like door stays open, ...).
Customers controls what security they choose to implement to protect the content, platform, applications, systems and networks (same thing that in a datacenter).

But the model changes for different service types:

- infrastructure: EC2, EBS, Auto scaling, VPC. Customer controls the OS and configure/operate any identity management system that provides access to the user layer of the virtualization stack
- container: (RDS, EMR, Elastic Beanstalk, ...) even if they run on EC2, we sometimes don't manage the OS or the platform layer (AWS manages PHP updates with Elasticbeanstalk for instance). Customer still responsible for setting up and managing network controls (firewall rules) and managing platform level identity and access management separately from IAM. 
- abstracted: high level storage, DB, messaging services (S3, Glacier, DynamoDB, SQS, SES, ...). AWS manages the OS, we just access the endpoints using AWS APIs (but we still need to control bucket policies for S3 and so on).

### AWS Security Responsabilities

global infrastructure
hardware, software (hypervisors, RDS operating systems, ...), networking and facilities
managed services (S3, DynamoDB, ...)

=> compute, storage, DB, networking, regions, AZ, edge locations (anything that we don't have access to)

### Customer Security and Responsabilities

Infrastructure as a service (IaaS)
updates and security patches
configuration of the AWS provided firewall (VPC rules, security groups, network ACLs, ...)

=> customer data, access management for applications, OS, network & firewall config, encryption, authentication integrity, server side encryption, network traffic protection

## AWS Artifacts

on-demand downloads of AWS security and compliance documents (AWS ISO certs, Payment card industry (PCI), Service Organization Control (SOC) reports). Can submit security and compliance documents (**audit artifacts**) to auditors or regulators to demonstrate security and compliance of the AWS infrastructure and services that we use.
=> service to download documents from AWS

## Best practices

* separate accounts as much as possible (prod, dev, audit) with always the minimum rights required
* use consolidated billing for accounts -> creates a single bill, track payments, reserved instance, capacity reservation, pay less on the volume
* implement, automate and validate cost controls
* implement and manage AWS resources auditing and validation
* apply appropriate AWS account and billing setup options based on business requirements
  * resource tagging
  * detailed billing reports
  * CW metrics and alarms
  * AWS Cost Explorer
  * Budgeting
  * Trusted Advisor
  * CloudTrail, AWS Config, AWS Config rules
* use Roles as much as possible (user, service, instance)
* use Trust Policy -> who can assume the role
* use Cross-Account access (trusting account, trusted accounts)
* Secured and easy user management with Cognito
* do not create too many IAM users, use Roles with SAML, OpenID, Cognito, ...
* Permissions policies -> what the role can do, managed policies, inline policies
* for S3, create resource based policies, grant access directly to the resource, specify conditions, resources, users
* users should use a role to access production, same for security team
* segregation of duties: assume a role, cross account, within an account, organizations
* Data protection
  * in transit: encryption TLS, VPN, Amazon Certificate Manager (generates public certificates)
  * at rest: sitting on the disk drive, encryption (EBS, RDS, S3, ...)
  * KMS: highly integrated into all services. Master keys never made available outside of the service. Data keys can be generated which are much easier to manage
  * Cloud HSM: higher validation than KMS can provide, single tenant user device, customers generate the key information, AWS is custodian of the device but can't decrypt their key information
* server side encryption
  * AWS Managed Key: S3 manages that key and controls the rotations, could be backed by KMS
  * Cloud HSM: customer brings key stored on prem or one from a managed service
  * EBS volumes: support KMS managed keys, we create a master key and a volume key, metadata stored onto the volume, not the actual key, volume is mounted to the EC2 instance, volume requests access to decrypt that volume that was contained within that metadata
  * all objects in Glacier are automatically encrypted
* RDS keys
  * AWS KMS keys
  * TDE for Oracle and MS SQL
  * The keys for Amazon Redshift could come from KMS or CloudHSM
* SSL termination as far as possible, preferably at EC2 level
  * at load balancer: certs stored in IAM, offload work to ELB tier, single SSL cert per load balancer
  * at EC2: real end to end encryption
  * Server name indication (SNI)
  * allows multiple IP addresses terminating different domain certificates, while valid for SSL
  * DNS records point to ELB or CloudFront
* security groups
  * per instance granularity
  * stateful = simpler to apply rules
  * inter service communication
* NACLs
  * subnet boundaries only
  * ALLOW and DENY rules
  * IP ranges only
  * block malicious traffic
* Host firewalls
  * central or distributed control
  * IDS, IPS functions
  * Scalability

## A/B testing

Closely related to Blue/Green deployments.

Randomized experiment with two variants, A and B. It is a way to compare two versions of a single application, calculating responses and determining which version is better. Version A might be the currently used version while version B is modified in some respect.

Common implementations in AWS:

* application load balancer sending traffic to the A/B apps
* CloudFormation template which creates an elastic Beanstalk application for both A/B (Route 53 weighted round robin for traffic distribution)
* CloudFront with Lambda@Edge. Create two CloudFront origins in S3. Lambda@Edge allows running lambda function at edge locations of the CloudFront CDN supplying intelligence at the front-end and routing traffic appropriately.

## Scenarios

### Scenario 1: CloudWatch 1

Q: send EC2 logs to CloudWatch, store logs durably and after 60 days send to long term storage

A: We need the CloudWatch Logs agent installed on the EC2 to send the logs to CloudWatch. Durably means S3 and long term storage means Glacier. We must use a lifecycle policy to move the logs from S3 to Glacier after 60 days

### Scenario 2: CloudWatch 2

Q: Using CloudWatch, we need to capture 500 errors from our web server and notify on-call engineer

A: We need the CloudWatch Logs agent installed on the EC2 to send the logs to CloudWatch. Notification of on-call engineer would be an SNS topic where the engineer are subscribed to. If we need to extract information from our logs to get the error 500, we need to create a log group and a filter.

### Scenario 3: Auto scaling 1

Q: bootstrapping instances in ASG takes 10 minutes. Instances are reported as in-service before bootstrapping completes and we are getting alarms

A: We don't have enough information about the bootstrapping process to know if we could solve it problem with a pre-baked AMI. We should create a Lifecycle hook on starting instance in the ASG (pending: wait). Once the bootstrapping is finished (use CONTINUE), send a signal to move it to pending: complete else an error. Default timeout is 60 minutes so we should be fine, no need for manual heartbeat.

### Scenario 4: Auto scaling 2

Q: CF to deploy app in an ASG; The ASG is at its maximum 6 instances due to high CPU utilization and it is still too high. We decide to upgrade our instances from T2 to C3. How can we do this no downtime ?

A: We want to execute our solution in CloudFormation. With an autoscaling group and the need to upgrade our instance types, we can create a new launch configuration since we cannot update launch config. Since there is the keyword "no downtime", we need to use the update policy in CloudFormation to use rolling updates (AutoScalingRollingUpdate) and not all at once. We then update the stack with the new CF template.

### Scenario 5: Beanstalk 1

Q: Work for large software company with a very diverse list of programming languages and platforms. The overriding requirement is to be able to deploy all the applications quickly using Beanstalk and to have high availability. How can we do this ?

A: High availability is a key phrase so there is definitely an auto scaling group involved maybe fronted by an ELB. Since we don't have the list of programming languages and platforms, we can't know if some of these are not supported by Beanstalk. In doubt, we should use Docker with Beanstalk. Quickly is also an important keyword as docker containers can start quickly.

### Scenario 6: Beanstalk 2

Q: We have deployed a Java app in a beanstalk environment. Now we have created a script to force HTTPS on Apache Web Server. What's the best way to deploy the script ?

A: Save script with .config at the end in the .ebextensions folder. Beanstalk will automatically apply the update.

### Scenario 7: CloudFormation 1

Q: We have a single CF template for the company infra, a multi tier web application. The web, database and security teams are in conflict over editing the template. How can we give each team separate parts of the template to manage.

A: The CF template should be split into multiple independent CF templates, one of the web layer, one for the database layer and one for the security of the application. These templates should be nested into a common CF template.

### Scenario 8: CloudFormation 2

Q: We are building a web server using a CF template. We add a long running script to the user data. What can we do to ensure that the script has finished and the server is up and running before it is added to the load balancer.

A: we would use WaitCondition and WaitHandle to sync our stack creation and use cfn-signal once the script is finished or an error.

### Scenario 9: EC2 1

Q: We have an app on EC2 instances. We need to securely store DB connection information (not hard coded in our app).

A: Secured and storage -> DB connection info should be stored in S3 with an IAM role (read access) that can be used by the EC2 instance to retrieve them

### Scenario 10: EC2 2

Q: we have an ASG of EC2 instances that we need to bootstrap. We need a highly durable, secure storage for our bootstrapping files and choose S3. How do we retrieve this information.

A: Pre-bake an AMI which creates the EC2 instances with an IAM role which allows read access to the bucket. Retrieve the bootstrapping file programmatically from the instances.

### Scenario 11: OpsWorks 1

Q: We are creating an OpsWorks stack to host our application. We have created the stack, added Layers including an Application Layer and add an instance to the Layer. But the instance never reaches a ready state and deployment fails, what could be wrong ?

A: When an instance starts in OpsWorks, it builds instance user data based on the OS type. OpsWorks installs the agent (downloaded from S3). S3 is not in our VPC so we need internet access to retrieve it so there is a potential problem with a missing internet connection. => instances must have a public IP or an elastic IP address, this is done when setting up the layers.

### Scenario 12: OpsWorks 2

Q: We are managing an OpsWorks stack. We have a new requirement to perform Blue/Green deployment to greatly minimize downtime. How can we implement this in OpsWorks ?

A: Clone the stack, update the new stack, do some testings on the new stack (green), once it is validated, replace the existing stack with this one witch a DNS switch in Route 53 using ALIAS.

## Continous deployment

Continous Deployment -> can be automated or manual action to deploy (QA, pre prod, prod) after successful tests

### Deployment process

important:

- pro and con of each deployment type
- when each should be used
- limitations of each
- how quick is deployment
- how quick is rollback
- how each deployment type impacts our applications
  => not all AWS services support all deployment types

**Single target deployment**: one step deployment, smal dev projects, legacy or non highly available infra. Testing opportunity is limited, rollback involves removing the new version and installing the previous

**All-at-Once deployment**: in one stage, deploy one binary onto all targets, more complicated than single target, often requiring orchestration tooling. Still shares the negatives of single target (no ability to test, small deployment outages and less than ideal rollback). **In CodeDeploy, it is called "In-Place" deployment.**

**Minimum in-service deployment**: specify a minimum number of healthy targets that will not be touched by the deployment, deploy on as many targets as possible while respecting the minimum in service targets.
A few moving parts, orchestration and health checks are required.
=> allows automated testing, deployment targets are assessed and tested prior to continuous
=> Generally no downtime
=> often quicker and less stages than rolling deployment

Several steps:

1. Initial build stage -> 5 targets healthy
2. Deployment stage 1 -> keep 2 targets healthy (in different AZ for HA), update the 3 others
3. Deployment stage 2 -> when 3 deployed are healthy, update the 2 remaining
4. Deployment complete -> all 5 targets have been updated

**Rolling deployment**: 
X number of targets are updated each time until all the targets have been updated
deployment happens in multiple stages, number of targets per stage is user defined
moving parts, orchestration and health checks are required
overall applicable health isn't necessarily maintained
allows automated testing, deployment targets are assessed and tested prior to continuing
generally no downtime, assuming number of targets per run isn't large enough to impact the application
can be paused, allowing limited multi version testing (combined with small targets per stage)

For some time, we have different versions running in parallel.

Several steps:

1. Deployment stage 1 -> 2 targets out of 5 are being updated
2. Deployment stage 2 -> when 2 targets healthy, pick 2 other targets to update, 1 remaining
3. Deploymen stage 3 -> when 4 targets healthy, pick last one for update
4. Deployment complete -> all 5 targets are healthy

**Beanstalk has rolling and rolling with additional batch. CodeDeploy has a variation of an in-place deployment with patterns like OneAtATime and HalfAtATime.**

**Blue green deployment**: 
production is blue, when new deployment, exact copy of production is created (green), traffic still going to blue
the copy is updated (green), when successful, traffic is directed towards green which becomes the new production

requires advanced orchestration tooling
carries significant cost - maintaining 2 environments for the duration of deployments
deployment process is rapid - entire env (blue or green) is deployed all at once
cutover and migration is clean and controlled -> DNS change
rollback is equally as clean -> DNS change
health and performance of entire green environment can be tested prior to cutover
using advanced template systems, such as cloud formation, entire process can be fully automated
=> this process is binary with a 100% shift at the end if successful
=> not done for testing a development as the goal is a full migration

**=> this is different than A/B testing where both are running and traffic goes to both environment to see which one works better**

**=> BeanStalk supports immutable and blue/green deployment patterns. CodeDeploy supports blue/green pattern.**

### A/B testing

A/B testing sends a percentage of traffic to Blue (current production) and a percentage to green (new version of the application)
A/B testing can also be used for a deployment. If the tests are successful with the new version, all the traffic can be directed to green

example:

1. Env starts with 100% traffic directed to current (blue) env
2. when green deployment completes, the distribution of traffic is changed to direct a small amount at the new green environment (10%-90% blue)
3. as confidence builds, distribution is reversed (90%-10% blue)
4. finally, 100% traffic is directed at green
5. remove the blue environment eventually

=> crucial to understand: with A/B testing, the end goal is not necessarily a complete deployment, we can just use it for testing (performance, reliability). The ending decision (new prod vs rollback) is based on feedback of the testing users
=> allows gradual performance/stability/health analysis

If bugs are detected, rollback can be enacted quickly and the damage caused by the failed update is minimised

A/B testing with AWS:

- generally uses Route 53
- two records are created (one pointing at A, the other at B)
- can have traditional round robin (50-50) or weighted round robin (weight for each environment)
- **based on DNS so caching and other DNS related issues can impact the overall accuracy of this technique**

### Bootstrapping

process during which we start a base image (ISO, AMI, ...) and via automation build on it, we create a more complex object

This can be achieved with "cloud-init" (canonical) or "cfn-init" (more complex init from CloudFormation)

With an AMI based approach, it is possible that we need a large number of AMI's if we want several custom images with minor changes.

To prevent that problem, we keep multiple base AMI, patches/settings modules, several versions of the application in S3 (or somewhere else) and we create a bootstrap script that takes several parameters (the AMI, what we want, the version we want, ...) to create a custom image.
=> scripts create custom image using AWS API or other tools like cloud-init (similar to Chef, all the components must be modular)

**=> pro/cons**
AMI pro (fast to boot), cons (low customization)
Bootstrap cons (slower to boot), fast (high customization)
=> we can have a mix of both, AMI with medium default config + bootstrap

### Immutable architecture

replace infrastructure instead of upgrading/repairing it
with mutable infra, it is possible to have different version of the same initial server running due to manual intervention

AWS:

- treat servers ars unchangeable objects
- don't diagnose and fix; throw away and recreate
- nothing is bootstrapped (except AMI creation), nothing is changed, an image for every version, pre-created, ready to go

### Containers and dockers

Traditional VM -> contains everything (guest OS, dependencies, apps, VM), OS takes a large size, density compromises (hardware, host OS, hypervisor, lots of VM)

Container -> contains the application and dependencies (lightweight), size mostly comes from the application, higher density and improved portability by removing the per container guest OS, faster to start than a VM
Benefits: 

- escape from dependency hell
- consistent progression from DEV -> TEST -> QA -> PROD
- isolation - performance or stability issues with App A in container A won't impact App B in container B
- resource scheduling at the micro level -> only what the app needs to run
- extreme code portability -> can run container on any host that can run docker
- micro services

Docker components:

- Docker image: an ISO/AMI, read only, stored locally or registry, has a base image
- Docker container: contains everything that the apps need to run, created from docker image
- Layers / Union file system: docker combine layers into a single image, when a layer is impacted by changes during build, only this layer and the layers that depend on it get rebuilt
- Dockerfile: list of instructions (one instruction = one layer) used to create a docker image
- Docker daemon/engine: create operating environment for the containers, in host daemon talks to clients to execute the commands to build, ship & run containers
- Docker client: interface between us and the docker engine (creation, manipulation and deletion of docker containers)
- docker registries/hub: storage of images, public or private

## Abuse Notification

AWS Acceptable Use Policy: https://aws.amazon.com/aup/

AWS sends an email with the actions they have taken against our resources if they violate AUP. AWS does not allow port scanning, IP spoofing, interception or pentesting of our resources without permissions

AWS has automated checks at edge and internal for abuse.

## Incident response

