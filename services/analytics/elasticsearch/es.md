# Amazon ElasticSearch Service

## General Info

easy to deploy, operate and scale Elasticsearch for log analytics, app monitoring, interactive search, ...

can be used with Kibana (plugin) for visualization

CloudWatch logs can be configured to stream log entries to Amazon ES in near real time through a CloudWatch logs subscription.

RDBMS vs ElasticSearch:

* Database - Domain/Cluster
* Table - Index
* Row - Document
* Column - Field
* Value - Value
* SQL - Query API
* Data inserts - Data indexing

With AWS ES:

* can change instance counts (scale out)
* change instance type (scale up more powerful instance)
* enable/disable dedicated master nodes 
* enable/disable zone awareness
* change storage configurations
* configure index snapshots
* change VPC settings to the cluster

this is one of the main service to use for logs analysis

## Concepts

**Domain/Cluster**: collection of nodes that store data, process search requests and index new data

**Nodes**: machines that contain data, process requests and index new data (EC2 instances)

**ElasticSearch**: open source search engine software developed by Elastic Co that is installed on all nodes of the cluster

**Kibana**: open source data visualization plugin that makes it easy to create visualization based on the data indexed in ES.

## Features and benefits

* automatically includes integrations with tools like
  * Kibana (data visualization)
  * Logstash (data ingestion)
  * Kinesis (ingest streaming data with Firehose)
  * and other AWS services like S3 or DynamoDB
* offers numerous configurations of CPU, memory, storage capacity, known as instance types
* provides up to 1.5 PB of instance storage
* controls access to the ElasticSEarch service with IAM, VPC and security groups
* Automated snapshots to backup and restore Amazon ES domains
* **Use CloudWatch for monitoring Amazon ES domain metrics and setting alarms**
* **Use CloudTrail to audit configuration API calls to Amazon ES domains**

## Use Case

* text search on indexed documents
* less than 1.5 PB storage, otherwise use S3
