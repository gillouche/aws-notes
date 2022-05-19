# AWS CodeCommit

## General Info

Managed, secure, scalable source control service that hosts private Git repositories.

Regional service.

Benefits

* fully managed by AWS
* stored encrypted and secured in AWS, auto encrypted at rest (AWS KMS) using customer specific keys
* git repository
* CodeCommit repositories are private
* scales seamlessly
* only private repositories
* integrated with Jenkins, CodeBuild and other CI tools
* collaborate on code
* HTTPS or SSH (encryption), auto encrypt at rest with KMS using CMK
* no limits on file types or the size of the repo: documents, source code, binary files
* integrate with other AWS services (IAM, CloudTrail,CLoudWatch, ...)
* migrate to CodeCommit from other git repositories
* use the same git workflows we are familiar with
* encrypted by KMS automatically (at rest and in transit)
* pay as you go
* supports pull requests before merging 
* integrated with IAM and can be used with other AWS services and in parallel with other repositories
* can migrate to CodeCommit from any git-based repository
* codecommit can trigger lambda on new code -> useful to investigate if credentials have been committed and send notifications
* need to configure git client to communicate with codecommit repositories -> need to provide IAM credentials that codecommit can use to authenticate us
* use IAM policies to control users/roles to repositories
* codecommit only supports identity-based policies, not resource-based policies
* can attach tags to codecommit resources or pass tags in a request to codecommit
  * codecommit:ResourceTag/key-name
  * aws:RequestTag/key-name
  * aws:TagKeys condition keys
* can trigger notifications in codecommit using SNS, Lambda, CloudWatch event rules 
  * pull request and comment events

Use cases for SNS/Lambda
* deletion of branches
* trigger for pushes that happen in the master branch
* notify external build system
* trigger Lambda function to perform codebase analysis

Use cases for CloudWatch Event Rules
* trigger for pull request updates (created/updated/deleted/commented)
* commit comment events
* CloudWatch Event Rules go into an SNS Topic

## Pre-requisites

Need IAM user (+ Access Key and Secret Access Key) to access CodeCommit

For the IAM user -> "Attach existing policies directly" to add "AWSCodeCommitFullAccess" to the user

Need to set up HTTPS git credentials for CodeCommit -> in IAM user -> Generate credentials for HTTPS. **We cannot choose our username or password. If we lose them, we need to generate them again.**

We can also upload SSH keys for CodeCommit

IAM supports CodeCommit with 3 types of credentials:
* Git credentials: IAM generated user name and password pair (HTTPS)
* SSH keys: locally generated public-private key pair that we associate to an IAM user (SSH)
* AWS access keys: credential helper included with the AWS CLI to communicate with CodeCommit repositories (HTTPS)

## Creation

Need a name.

Need to configure email notifications based on event types (optional) => SNS topic

* pull request update events
* pull request comment events
* commit comment events

Need to configure if we want HTTPS or SSH (need to specify the OS) to connect.

Need a role for the user with 

* IAMSelfManageServiceSpecificCredentials
* IAMReadOnlyAccess 

The user needs to generate Git credentials for the IAM user (console)

## Notifications

when configured, subscribed users receive emails about the events that we specify such as

* pull request update events
  * a pull request is created or closed
  * a pull request is updated with code changes
  * the title or description of the pull request changes
* pull request comment events
  * comment or reply to a comment in a pull request
* commit comment events
  * when someone comments on a commit outside of a pull request (lines of code in a commit, files in a commit, commit itself)
