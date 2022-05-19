# AWS Data Pipeline

## General Info

highly available web service that helps us reliably process and move data between different AWS compute and storage services (S3, RDS, DynamoDB, EMR) as well as 
on-premises data sources at specified intervals

**=> transform and process data at scale. should only be used for huge amount of data**

Used to create complex data processing workloads that are fault tolerant, repeatable and highly available. We don't have to worry about ensuring resource availability,
managine inter-task dependencies, retrying transient failures or timeouts in individual tasks.

Pipeline can be triggered on pipeline activation or on schedule.

Resources (EC2, EMR) are deleted after the pipeline is finished but we have the possibility to automatically delete them a certain number of days 
if they are still alive even if the job is done. => the pipeline is validated when created and warnings are sent to the console

Data Pipeline takes some time to process since it needs to start an EMR cluster (or EC2). This time is not a problem if we have a huge amount of 
data but it is not good for small dataset.

Destinations:

* S3
* RDS
* DynamoDB
* Redshift
* EMR

Data pipeline is just an orchestrator (retries on failures, ...), ETL actions are executed on EC2 managed by Data pipeline.

## Concepts

**Data node**: location and type of data that Data Pipeline activities use as input or output. Supported data nodes include:

* DynamoDBDataNode: DynamoDB table that has data for Hive or EMR activity, needed to specify the RCU available for processing as we don't want to take all the possible RCU from the applications
* SqlDataNode: SQL table, database, query that represents data for a pipeline activity
* RedshiftDataNode: Redshift table that data should be copied to
* S3DataNode: S3 location that contains data files for a pipeline activity

**Definitions**: determine the data pipeline tasks to run, schedules them and then assigns them to task runners. If tasks fail, they are re-tried or passed off to another task runner. These definitions are composed of:

* data nodes: the location of input/output data
* activities: definitions of work to perform on a schedule
* preconditions: optional conditions that must be true before an activity can run
* scheduling pipelines: determines the timing of events (like when the activity runs)
* resources: the computational resource (EC2 instance, EMR) that does the work the pipeline defines
* actions: things that are triggered when conditions are met (SNS notification on the success or failure of a pipeline)

## Processing
3 things that are affiliated with a scheduled pipeline:

* pipeline components
  * business logic of the pipeline
  * pipeline components are themselves contained inside a Pipeline Definition File
  * Examples of pipelie components include:
    * activities
    * data source
    * schedules
    * preconditions
* Instance (tasks): things to do that contain information on how a task runner should do something such as copying the data these instances are created from and the compiled pipeline components
* attempts: literally attempts to successfully complete a data pipeline task activity such as copying data; new attempts will continue until the set maximum number of retries is reached

There are also a Task Runner which is an application that checks AWS Data Pipeline for new tasks and then does those tasks, it can be:

* automatically installed on resources that Data Pipeline will create and manage for us
* installed on a compute resource that we manage such as an EC2 instance or on-premise hardware

## AWS Data Pipeline vs Glue
Glue

* very apache spark focus
* Glue ETL: run apache spark code, scala or python based, focus on ETL
* Glue ETL: do not worry about configuring or managing the resources
* Data Catalog to make the data available to Athena or Redshift Spectrum

Data Pipeline

* Orchestration service
* more control over the environment, compute resources that run code and the code itself
* allows access to EC2 or EMR instances (creates resources in our own account)


## Example
1. DynamoDB & RDS contain data for a dataset that we would like to perform ML on it
2. we want to move that data into an S3 bucket to be used by SageMaker
3. start AWS data pipeline that will spawn EC2 instances managed by Data Pipeline
4. the apps on EC2 will retrieve the data and store it in S3

## Resources
FAQ:  https://aws.amazon.com/datapipeline/faqs/