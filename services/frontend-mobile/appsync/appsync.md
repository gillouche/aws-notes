# AWS AppSync

## General Info
* fully managed service for GraphQL APIs
* securely connects to data sources like DynamoDB, Lambda, ElasticSearch and more
* add cache to improve performance, subscriptions to real time updates, client side data stores that keep offline clients in sync
* auto scale GraphQL API execution engine up and down to meet API request volumes
* can specify which portions of the data should be available real time using GraphQL Subscriptions
  * simple statements in the app code that tell the service what data should be updated in real time
* Amplify DataStore provides a queryable on-device DataStore for web, mobile and IoT devs
  * can be combined with AppSync to leverage advanced versioning, conflict detection and resolution in the cloud
  * allows auto merging of data from different clients as well as providing data consistency and integrity
* server-side data caching capabilities reduce the need to directly access data sources
* low latency delivery -> high speed in memory managed caches
  * can specify customizable expiration for data fields
* can use custom domain names with API to access GraphQL endpoint and real time endpoint
  * used with AWS Certificate Manager certificates
  * AppSync auto route the request to the associated API for handling

## GraphQL
* data language that enables client apps to fetch, change and subscribe to data from servers
* in a query, the client specifies how the data is to be structured from the server
* client query only the data it needs, in the format that it needs it in
* other feature called introspection: developers on a project discover the data available without requiring knowledge of the backend
* can be simple lookups, complex queries & mappings, full text searches, fuzzy/keyword searches, or geo lookups

## Security
* simple access can be protected by key
* IAM roles for more restrictive access control
* Cognito user pools for email/pw functionality
* social providers (Facebook, ...)
* enterprise federation with SAML
