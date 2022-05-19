# AWS Snowball Family

## General Info

* Physical devices for secure storage transportation
* Snowball client is software that is installed on a local computer and is used to identify, compress, encrypt and transfer data
* Uses 256-bit encryption (KMS) and tamper resistant enclosures
* Snowball (80TB, 50TB) petabyte scale
* Snowball Edge (100 TB) petabyte scale
* Snowmobile (up to 100PB per snowmobile) exabyte scale

Snowball is data transfer only, 80TB device
Edge is data transfer + compute -> use if we need to process data locally before returning it to AWS
If we have 100TB to move or if it takes more than a week, we should use snowball 

It is needed to create a job in AWS Snowball Management console and AWS prepares a snowball appliance for the job then shipped.

Physical device used for transporting many TB or PB of data into and out of AWS
Larged scale data transfers: fast, easy, secure
Need snowball client to manage transfers
Tamper resistant enclosure
256bit encryption by default
region specific, not for transporting data from one region to another

When to use:

- TB or PB data to upload
- no expensive upgrades to current network for one off transfer
- frequently experience backlogs of data
- physically isolated environment, bad internet or too epensive
- if it takes more than one week to upload the data

Snowball edge

- 100TB device
- onboard compute power which can be clustered to act as a single storage and compute pool **(not Snowboall)**
- designed to undertake local processing / edge computing as well as data transfer
- S3 compatible endpoint, supports NFS, can also run Lambda functions as data is copied to the device
- S3 buckets and lambda functions come pre-configured on the device (need to request to AWS before)

Common use cases:
* cloud data migration
* disaster recovery
* data center decommission
* content distribution: send data to clients or customers
* tactical edge computing: collect data and compute
* machine learning: run ML directly on the device
* manufacturing: data collection and analysis in the factory
* remote locations with simple data: pre processing, tagging, compression, etc

AWS Snowmobile: truck to move exabyte-scale data transfer, can transfer up to 100PB per Snowmobile. Data is then imported to S3 or Glacier.
Dedicated security personnel, GPS tracking, alarm monitoring, 24/7 video surveillance, optional escort security vehicle while in transit.
Data is encrypted with 256-bit encryption keys

Ways to optimize the performance of Snowball transfers
* use latest Mac or Linux snowball client
* batch small files together
* perform multiple copy operations at one time (multiple terminals, multiple instances of the agent, ...)
* copy from multiple workstations
* transfer directories, not files

When evaluating snowball vs internet migration
* snowball takes around a week to move from data center to S3
* check connection speed, evaluate

## Snowball Family
* Snowball and Snowmobile are used for migrating large volumes of data to AWS
  * slow internet, don't want to use internet bandwidth for migration
  * data imported to S3
* Snowball Edge Compute Optimized
  * provides block and object storage and optional GPU
  * use for data collection, ML and processing, and storage in environments with intermittent connectivity
  * no good internet
* Snowball Edge Storage Optimized
  * provides block storage and Amazon S3-compatible object storage
  * use for local storage and large scale data transfer
* Snowcone
  * small device used for edge computing, storage and data transfer
  * contains DataSync agent
  * can transfer data offline (move device physically) or online with the agent

## Performance

we can improve transfer speed from data source to snowball by:

* reducing local network use
* eliminating unnecessary hops between the Snowball appliance and the workstation
* using a powerful computer as the workstation
* combining smaller objects.
* using multiple snowball in parallel
* using multiple snowball clients in parallel and one snowball
* using multiple snowball clients in parallel and multiple snowball devices

## Security

physically secured

can use IAM to control what a user can do

integrated with KMS and AES256bit encryption

## Pricing model

service fee per job

extra day charges as required (first 10 days on site usage free)

data transfer

