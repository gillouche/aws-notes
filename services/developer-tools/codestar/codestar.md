# AWS CodeStar

## General Info

Can be used to rapidly orchestrate an end-to-end software release workflow using the other AWS developer services.

CodeStar uses CodePipeline, CodeBuild, CodeCommit and CodeDeploy with an integrated setup process, tools, templates and dashboard. 

Also supports Lambda:

* changes env with CloudFormation
* create resources at a stage and delete them at another
* swap CNAME values to achieve zero downtime
* deploy to ECS
* backup resources before building or deploying by creating an AMI snapshot
* notification (slack, IRC, ...)

Benefits and features

* project templates for various software projects and programming languages like Go, Node.js, Python, HTML, Java Spring, ...
* helps manage users and the access they require to interact with AWS services (saves us from having to create and manage IAM policies)
* integrate some IDEs with CodeStar
* Visualize and collaborate on our projects in the same place
  * app activity metrics like CPU utilization
  * JIRA Issue tracking
  * commit history and changes
  * continuous deployment details

CodeStar integrates with other AWS services 

* CodeCommit
* CodeBuild
* CodeDeploy
* CodePipeline
* CloudWatch
* Cloud9

Exam tip: If an exam scenario requires a unified development toolchain, 
and mentions collaboration between team members, synchronization, and centralized management of the CI/CD pipeline this 
will be CodeStar rather than CodePipeline or CodeCommit.

## Benefits and features
project templates for various projects and programming languages
* websites, web app, web services and alexa
* include code for getting started: Java, JS, PHP, Ruby and Python

Simplify project access: role based, AWS security best practices

Multi IDE supports: natively with Cloud9, Visual Studio, Eclipse

Free, only pay for resources (EC2, Lambda, S3 buckets)




