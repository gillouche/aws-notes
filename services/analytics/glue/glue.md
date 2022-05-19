# AWS Glue

## General Info

fully managed, serverless, extract transform and load (ETL) service used to prepare and load data for analytics. 

Glue discovers the data and stores the associated metadata (table definition and schema) in the AWS Glue Data Catalog.
Once cataloged, the data is immediately searchable, queryable and available for ETL, Athena, ...

can be used to migrate data from on-premises DB to AWS environment

Works with data lakes (data on S3), data warehouses (redshift) and data stores (RDS, EC2 db)

Lambda can trigger a glue job based on event in S3: only good if we have like one file every X time, not if we continuously have files

## Use cases
* discover properties of data, transform it and prepare it for analytics
* discover both structured and semi structured data stored in data lakes on S3, Redshift and other DB running on AWS
* provides a unified view of data via the Glue Data Catalog that is available for ETL, querying and reporting using services like Athena, EMR, Redshift Spectrum
* auto generate Scala or Python code for ETL
* serverless, no compute resources to configure and manage

## key components
- Glue Data catalog: managed service used to store, annotate and share metadata (hive metastore)
- Glue Crawlers and classifiers: scan data in supported repo, classify it, extract schema info from it and store metadata in Glue Data Catalog
- Glue ETL: can autogenerate Scala or PySpark scripts
- Glue Jobs system: managed infra to orchestrate ETL and transfer data to different locations. 
Jobs can be scheduled and chained or they can be triggered by events such as the arrival of new data. They sometimes add unnecessary complexity.

Easy setup, we can schedule ETL jobs after crawlers for instance.

### Limitations
Note that Glue ETL is not really suitable for huge batch job with custom heavy process, for that it is better to use AWS batch.

## AWS Glue Data Crawler
crawler maintains partition definitions and schema versioning

Can crawl multiple data stores in a single runs; when done, it creates one or more tables in our Data Catalog.
ETL jobs in GLue use the Data Catalog tables as sources and targets.

The data stays in the repo (S3, Database that supports JDBC connection, DynamoDB table) but there is an AWS Glue data crawler 
that can go to a bucket, scan the data and extract schema => Glue does not store any data

Crawlers go through our data to infer schemas and partitions

* works for JSON, Parquet, CSV, relational store
* works for S3, Amazon Redshift, Amazon RDS

Crawler can run on a Schedule or on demand (hourly, daily, weekly, ... custom) and they need an IAM role/credentials 
to access the data stores (Redshift or RDS)

We can crawl multiple data sources and create a single view/endpoint of the data.

Awesome tool to keep the data updated in Athena tables. Since the data schema does not change, the daily data is readily available for SQL queries in Athena
as soon as it arrives.

If we read from a bucket, we can exclude files with the exclude pattern "**.metadata" for instance (crawler definition)

Glue Crawlers can help build the Glue Data Catalog

### S3 partitions
Glue crawler will extract partitions based on how S3 data is organized
=> we need to think up front about how we will be querying our data lake in S3

Example: devices send sensor data every hour

* do we query primarily by **time ranges**? -> organize buckets as s3://mybucket/dataset/yyyy/mm/dd/device
* do we query primarily by device? -> organize buckets as s3://mybucket/dataset/device/yyyy/mm/dd

Based on our partitions, Databases tables will be created for us to query. The partitions will be detected easily (partition_0, ...).
If we are not happy with the default name, we can edit the schema ourselves but we can also delete some column if we want.

Organizing data by date using S3 prefixes allows Glue to partition the data by date, which leads to faster queries done on date ranges.

### Create a crawler
In the console, we create a crawler, give it a name and optionally tags, description, security configuration and classifiers.

We then configure the crawler source type:

* data stores: new datasource in S3 for example
    * S3
    * JDBC
    * DynamoDB
* existing catalog tables

The datastore can be in our account or another account. We then specify the path s3://bucket/blabla 
Note that we can have exclude patterns to not crawl a whole bucket.

Once configured, we can add another datastore if we want. We then need to choose an IAM role (existing or create).
To create a role we need "CreateRole", "CreatePolicy" and "AttachRolePolicy" permissions.

Afterwards, we configure the frequency of the crawl

* on demand
* hourly / daily
* specific days 
* weekly
* monthly

Finally, we need to choose the output of the crawler; the database can be existing or created

### Run a crawler
From the console, select crawler and run. The infrastructure is created for us to execute the crawler.

Note that after the crawling, we cannot see the data in the tables, we can just see the schema. For the querying, 
we need Athena.

## Glue ETL (Extract Transform Load)
Not meant for streaming data, only batch jobs. Fully managed, cost effective, pay only for the resources consumed

Jobs are run on a serverless Spark platform

AWS Glue ETL jobs can interact with a variety of data sources inside and outside of the AWS environment.

We can generate ETL code in Python or Scala that we can modify. Python uses Python Shell (numpy, pandas, sklearn); PySpark uses Python API of Apache Spark.
We can also provide our own Spark or PySpark scripts. 

Datasource comes from Glue Data Catalog.

Take data out of a datasource (or multiple), do some transformation and load it into another data source

Glue ETL is best suited for batch ETL use cases and it is not meant to process near real time data. For real time data,
firehose can trigger lambda that does the transformation and copy to S3

Glue cannot write the output in RecordIO-Protobuf format. Lambda is not suited for long-running processes such as 
the task of transforming 1TB data into RecordIO-Protobuf format. 

Targets can be S3, JDBC (RDS, Redshift), or in Glue Data Catalog

### Transformations
Transform data, clean data, enrich data (before doing analysis).

Bundled Transformations:

* DropFields, DropNullFields - remove null fields
* Filter - specify a function to filter records
* Join - enrich data
* Map - add fields, delete fields, perform external lookups

Machine Learning Transformations:

* FindMatches ML: identify duplicate or matching records in our dataset, even when the records do not have a common
unique identifier and no fields match exactly

=> This will not require writing any code or knowing how machine learning works.

We can also do format conversions: CSV, JSON, Avro, Parquet, ORC, XML

We can also use any Apache Spark transformations (ex: K-Means)

### ETL data source connectors
* nosql
    * documentdb
    * dynamodb
    * mongodb
* relational
    * mysql
    * oracle
    * postgresql
    * sql server
    * Redshift
* other
    * orc: data in S3 with Hive Optimized Row Columnar file format
    * parquet: stored in S3 but parquet file format
    * s3

## ML capabilities
basic ML capabilities under the hood of Glue

Let's say that we have the same person in two different datasets but with small differences (Mike - Michael), we can
train a model inside of Glue to detect duplicates in the resulting dataset.

The goal is not to change data but to extract new info from the input data. For a recommender systems, we could
merge both records since they come from the same person. **We don't use that to fix the data, only to use it in a
downstream process.**

AWS Glue ML Transforms job can perform deduplication in a serverless fashion. This is the least significant for development and maintenance effort.
Spark on EMR and Lambda could do the same job but they need more maintenance.

## Glue Jobs
Spark programs run on a serverless Spark Cluster

Transform type can be:

* change schema: change schema of our source data and create a new target dataset
* find matching records: use ML to find matching records with source data, optionally we can "remove records"

For a job, we need to specify the worker type and the number we want

* standard
* G.1X (recommended for memory intensive jobs)
* G.2X (recommended for ML jobs transform)

Where to store the data (S3, JDBC), which format (Parquet, ...), target path

Then map the source columns to target columns (if we wanted to change the schema)

Next a Glue job ETL is generated in the console (generated python script) that we can edit if we want.

We then save and run the job.

we can use the Glue Scheduler to schedule jobs (Glue ETL, ...)

We also have **Glue Triggers** to automate job runs based on events

## Glue Data Catalog
Metadata repository for all our tables (index in S3)

* automated schema inference
* schemas are versioned

Integrates with Athena or Redshift Spectrum (schema & data discovery)

The schema can then be used by 

* Amazon Redshift
* Athena then QuickSight
* Amazon EMR

## Security
Best methods to control access to the Glue Data Catalog resources (DB, tables, connections):

* Use AWS IAM identity based policies (attached to user, group, role, service)
* Use AWS IAM resource based policies (attached to resources) -> resources include DB, tables, connections and user defined functions along with the Data Catalog API that interact with these resources

## Resources
Glue FAQ: https://aws.amazon.com/glue/faqs/

