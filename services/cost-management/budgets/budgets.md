# AWS Budgets

## General Info

* used to track how close our current costs are to exceeding the set "budget" for a given billing period (not necessarily a full month) => based on activity pattern of last month and current month billing
* We can aggregate cost level (for example all costs) or further refined to include only those costs relating to specific cost dimensions or groups of cost dimensions including Account, Service, Tag, AZ, Purchase Option (reserved) and/or API operation 
* Use AWS Budgets to create a budget for reserved instance coverage and set the threshold to X%. Configure alert based on that
* Budgets are at the payee (consolidated billing owner) level 
* Budgets can be tracked at the monthly, quarterly or yearly level, can customize start and end dates 
* Budgets are updated every 24 hours 
* Budgets do not show refunds 
* Budgets are not automatically created by AWS 
* Budgets can be compared against AWS "estimated" costs to see how much budget is left over (machine learning algorithm based on activity pattern of last month and current month billing)
* Budgets can work with SNS/CloudWatch for billing alerts to receive notifications if we have gone over our designated budget or even if we are "close" to going over 
* AWS Credits currently "skew" Forecasts provided by AWS 
* The dashboard shows the current budget vs the set budget and see how close we are from it
* **This is only to monitor, this doesn't stop us from going over the set budget**
* easy to determine costs for each team => IAM policies to enforce tagging on resources and budgets based on tags
* Create budgets and be notified when forecasted is bigger than budgeted
* can set custom budgets (set custom usage and reservation budgets)
* can configure alerts
* integrated with other AWS services: includes Cost Explorer Chatbot and Service Catalog
* can use AWS Budgets to track service costs and usage within AWS Service Catalog.
  * can also associate budgets with AWS Service Catalog products and portfolios
* budget type
  * Cost budget: monitor the costs and receive alerts
  * Usage budget: monitor usage of onr or more specified usage types and usage type groups and receive alerts
  * Reservation budget: track reserved instance utilization or RI coverage associated with our resources (EC2, RDS, Redshift, ElastiCache and Elasticsearch)
  * Savings Plans budget

