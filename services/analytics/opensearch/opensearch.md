# AWS OpenSearch

## General Info
* successor of Amazon ElasticSearch service
* open source, distributed search and analytics suite based on ES
* ES = distributed search and analytics engine built on Apache Lucene
* popular search engine commonly used for log analytics, full text search, security intelligence, business analytics

## Features
* perform log analytics interactively
* perform real time app monitoring
* website search
* performance metric analysis and more
* can choose a variety of open source engine options for OpenSearch cluster (latest OpenSearch and many versions of ALv2 ES)

## Deployment and monitoring
* specify number of instances, instance types and storage options
* in place upgrades without downtime
* built-in monitoring and alerting with automatic notifications
  * webhooks, Slack, SNS, Amazon Chime
* can configure alerts using Kibana or OpenSearch Dashboards and the REST API
* query language
  * Domain Specific Language (DSL)
  * SQL queries with OpenSearch SQL
  * OpenSearch Piped Processing Language (PPL)
* tool integrations
  * Logstash
  * OpenTelemetry
  * ElasticSearch APIs
* can be launched into an Amazon VPC
  * can't switch between public and VPC
  * cannot do both a public endpoint or VPC
  * can't move to another VPC once created (can change subnet and security group settings)
  * access dashboard => users also need access to the VPC

## Security
* encryption of data at rest
* KMS for storage and management of encryption keys
* encryption uses AES-256
* encryption node-to-node communications using TLS 1.2
  * once encryption enabled, cannot disable it -> must create a new domain
* 3 types of access policies:
  * resource based policies (like a bucket policy with a principal and which ES resource)
  * identity-based policies (attached to user, roles, ...)
  * IP-based policies (like if we have a condition on IP address for a resource)
* security at the index, document and field level
* authentication through SAML and Amazon Cognito