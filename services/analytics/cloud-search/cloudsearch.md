# AWS CloudSearch

## General Info

Fully hosted solution provided by AWS used for indexing documents and information contained within the documents for search within an application

provides search features similar to Apache **SOLR** and CloudSearch is powered by SOLR

Search features include:

* full text search
* boolean search
* prefix search
* range search
* term boosting (assign higher importance to specific key words)
* faceting (essential drill down and filter searches)
* highlighting (highlights all items found on a paged based off of the search)
* autocomplete suggestions

For example, upload file to S3, CloudSearch indexes the content and we can search it later on.

Document types that can be indexed by CloudSearch:

* CSV
* PDF
* HTML
* Excel
* PowerPoint
* Word
* Regular Text

**We don't specify a list of PDF files to search.** CloudSearch automatically builds some kind of database with the content of all the files and we search through that database.

CloudSearch can also be used to search DynamoDB tables

* when updates to DynamoDB data occurs , send the updates to CloudSearch (lambda)
* periodically send the updates to CloudSearch (lambda)

**The CloudSearch data is indexed within CloudSearch. If changes occur to indexed items, they will need to be re-uploaded to CloudSearch for indexing.**

**In the case of DynamoDB, we offload the search from DynamoDB to CloudSearch. The inconvenient is that the data might not be up-to-date in CloudSearch compared to DynamoDB.**

## Scaling

automatic scaling based off of the increase in data and search load on the nodes

can manually scale out to additional nodes in the interface if there is an anticipation of increase in search traffic

Multi AZ available by the click of a button to automatically add high availability

The Core of CloudSearch is just running software on EC2 instances so there are costs associated with those nodes which is the cost of CloudSearch

## Use case

search and sort functionality on large scale website
