# Amazon FSx

## General Info
fully managed 3rd party file systems
* windows
* high performance computing (HPC)
* ML
* electronic design automation (EDA)

Amazon FSx automates admin tasks, hardware provisioning, software config and backups

4 file systems:
* Amazon FSx for Windows File Server for Windows-based applications 
* Amazon FSx for Lustre for compute-intensive workloads. 
* Amazon FSx for NetApp ONTAP. 
* Amazon FSX for OpenZFS.

## Amazon FSx for Windows File Server
* native windows file system
* built on Windows Server: support SMB protocol, Windows NTFS, Microsoft AD integration
* SSD storage for fast performance with low latency
* built for critical workloads like home directories, media workflows, and business applications
* helps optimize TCO with data deduplication reducing costs by 50-60% for general purpose file shares
* can use user quota to monitor and control costs

### Details and benefits
* highly available: data replicated within an AZ -> self healing infra for components
* multi AZ: can be deployed in multi AZ as option -> active/standby file server in separate AZ, synchro replication to the standby
* supports windows native file system features: ACL, shadow copies, user quotas
* NTFS file systems that can be accessed from up to thousands of compute instances using the SMB protocol
* up to 2GB/second throughput per file system, hundreds of thousands of IOPS and consistent sub-millisecond latencies
* can connect to EC2, VMware cloud, Amazon Workspaces, Amazon AppStream 2.0 instances
* auto encrypt at rest and in transit
* cloudtrail support

## Amazon FSx for Lustre
* high performance file system, fast processing of workloads such as ML, HPC, video processing, financial modeling, electronic design automation (EDA)
* need fast data and scalable file system interface -> datasets stored on long term data stores like S3
* hundreds of gigabytes per second of data, millions of IOPS, sub millisecond latencies
* works natively with S3, can read and write from S3 then delete file system
* can also burst data processing workloads from on-premises to AWS -> can access FSx file system over direct connect or VPN
* performance is based on the size of the filesystem

### Details and benefits
* open source parallel file system designed for high performance workloads
* high throughput for processing large amounts of data, performs operations with consistently low latencies
* store data across multiple networked servers that thousands of compute instances can interact with concurrently
* POSIX compliant file system interface
* file access to thousands of EC2 for processing genomics, seismic exploration and video rendering

### Security
* encrypted at rest
* open source Lustre client
* compatible with linux based AMI
* access FSx file system from endpoints in VPC -> enables us to isolate file system in our own virtual network
* can configure security group
* supports IAM (users, groups, tags permissions)

Can be deployed in persistent or scratch
* persistent
  * long term use cases
  * HA in one AZ and self healing
  * 50, 100, 200 MB/s per TiB of storage
  * Burst up to 1300Mbits/per TiB (credit system)
* scratch
  * best perf for short term and temporary use cases
  * no HA or replication
  * larger file systems require more servers and disk -> more chance of failure
  * auto heals when hardware failure occurs
  * min size is 1.2 TiB with increments of 2.4 TiB
