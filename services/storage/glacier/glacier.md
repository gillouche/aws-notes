# Amazon S3 Glacier

## General Info

When object archived -> storage class = Glacier
When user restores:

- object available only for the duration specified in the restore request
- if user wants to modify that period, he has to raise another restore request with updated duration
- storage class will be Glacier for the restored object

Glacier automatically encrypts data with 256bit AES.

Data stored as archive which can be a single file or combine several files to be uploaded as a single archive.
Retrieving archives from Glacier requires the initiation of a job. It takes 3-5 hours to retrieve data from Glacier (Restore API). 3 options to retrieve archives ranging from a few minutes to several hours: Expedited (1-5 minutes), standard (3-5 hours) or bulk (5-12h).
An archive has a limit of 40TB, can use multipart to upload but there is no limit on the numbers of archives we can have in Glacier.

We can directly upload to Glacier or use a Lifecycle from S3.

We can specify a byte ranges to retrieve from an archive in case we don't want to download all the archive.

We can organize archives in vaults. Need to create an IAM policy with specific accounts who can access it.
We can specify controls such as "undeletable records" or "time-based data retention" in the vault lock policy and then lock the policy from future edits.

When uploading an archive, only get SUCCESS when the data has been copied in multiple facilities.

self healing by Glacier

When we restore from Glacier, it is a copy to S3 Reduced Redundancy Storage (RRS) or Standard IA for a specified retention period. Can be notified with S3 Event notification when copy is done.

When using Glacier as a storage class in S3, we use the S3 API and when using "native" Glacier, we use the Glacier API.
Objects archived to Glacier using S3 lifecycle policies can only be listed and retrieved by using the S3 API or the S3 console.
We can't see them as archives in an Amazon Glacier vault.

Amazon S3 Glacier provides query-in-place functionality to run powerful analytics directly on the archive data at rest.

S3 Glacier Instant Retrieval
* Data retrieval in milliseconds with the same performance as S3 Standard 
* Designed for durability of 99.999999999% of objects across multiple Availability Zones 
* Data is resilient in the event of the destruction of one entire Availability Zone 
* Designed for 99.9% data availability each year 
* 128 KB minimum object size 
* Backed with the Amazon S3 Service Level Agreement for availability 
* S3 PUT API for direct uploads to S3 Glacier Instant Retrieval, and S3 Lifecycle management for automatic migration of objects

S3 Glacier Flexible Retrieval (Formerly S3 Glacier)
* Designed for durability of 99.999999999% of objects across multiple Availability Zones 
* Data is resilient in the event of one entire Availability Zone destruction 
* Supports SSL for data in transit and encryption of data at rest 
* Ideal for backup and disaster recovery use cases when large sets of data occasionally need to be retrieved in minutes, without concern for costs 
* Configurable retrieval times, from minutes to hours, with free bulk retrievals 
* S3 PUT API for direct uploads to S3 Glacier Flexible Retrieval, and S3 Lifecycle management for automatic migration of objects 

Amazon S3 Glacier Deep Archive (S3 Glacier Deep Archive)
* Designed for durability of 99.999999999% of objects across multiple Availability Zones 
* Lowest cost storage class designed for long-term retention of data that will be retained for 7-10 years 
* Ideal alternative to magnetic tape libraries 
* Retrieval time within 12 hours 
* S3 PUT API for direct uploads to S3 Glacier Deep Archive, and S3 Lifecycle management for automatic migration of objects

Glacier must complete a job before you can get its output.

Requested archival data is copied to S3 One Zone-IA.

Following retrieval you have 24 hours to download your data.

Glacier does not archive object metadata; you need to maintain a client-side database to maintain this information.

Archives can be 1 byte up to 40TB

Archive retrieval:

* Expedited is 1-5 minutes retrieval (most expensive). 
* Standard is 3.5 hours retrieval (cheaper, 10GB data retrieval free per month). 
* Bulk retrieval is 5-12 hours (cheapest, use for large quantities of data).

To retrieve specific objects within an archive you can specify the byte range (Range) in the HTTP GET request (need to maintain a DB of byte ranges).

When you restore you pay for: The Glacier archive, The requests, The restored data on S3.

## Pricing model

* storage (per GB per month)
* data transfer out (per GB per month)
* requests (per thousand UPLOAD and RETRIEVAL requests per month)
* number of lifecycle transition requests
* objects must stay a minimum of 90 days in Glacier else we pay for 90 days even if we delete after 30 days

can retrieve up to 10GB for free each month.
