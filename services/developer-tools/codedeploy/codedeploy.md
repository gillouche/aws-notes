# AWS CodeDeploy

## General Info
Similar tools: Ansible, Terraform, Chef, Puppet

CodeDeploy automates deployments of our applications to EC2, ECS, Lambda and even on-premises environments.
* EC2/On-Premises -> in place or blue/green deployment
* Lambda -> canary, linear or all-at-once configuration
* ECS -> blue/green, canary, linear, all-at-once configuration

=> AWS Lambda and ECS **CANNOT** use an in-place deployment type and blue/green only for EC2, not on-prem

CodeDeploy does not provision the resources -> it only deploys applications, not EC2 instances

EC2 instances are identified by CodeDeploy by using tags or an ASG name => must have the correct IAM instance profile attached, need the CodeDeploy agent 

We can deploy code, lambda functions, web and config files, executables, packages, scripts, multimedia files. Can deploy application content that runs on a server and is stored in S3 buckets, GitHub repo or BitBucket repositories.

Benefits of CodeDeploy:

* automated deployments
* minimize downtime
* stop and rollback
* centralized control
* concurrent deployments

Requires **appspec.yml** -> must be at the root of the source code

can deploy app from S3, GitHub or Bitbucket

Major steps of CodeDeploy deployment: create application -> specify deployment group -> specify deployment configuraiton -> AppSpec file -> Deploy -> Check Results -> Redeploy as needed

CodeDeploy is very visual, we see the number of instances we have during deployment, the deployment process, which instances receive traffic and stuff like that. Especially with blue/green deployment.

Can deploy to EC2 instances, ASG, lambda functions, on-premises instances, ...

Pay as you go

Content must be on S3, Github or bitbucket repo

**CodeDeploy is really linked with our environment. For example, if we deploy to an ASG and we changed manually the desired capacity, CodeDeploy will be aware of the new deployment required on the instance and will trigger the installation of the app on the new instance.**

CodeDeploy can be connected to CodePipeline and use artifacts from there

## Blue/Green deployment
A blue/green deployment is used to update your applications while minimizing interruptions caused by the changes of a new application version. CodeDeploy provisions your new application version alongside the old version before rerouting your production traffic.

AWS Lambda: Traffic is shifted from one version of a Lambda function to a new version of the same Lambda function.

Amazon ECS: Traffic is shifted from a task set in your Amazon ECS service to an updated, replacement task set in the same Amazon ECS service.

EC2/On-Premises: Traffic is shifted from one set of instances in the original environment to a replacement set of instances.

Note: All AWS Lambda and Amazon ECS deployments are blue/green. An EC2/On-Premises deployment can be in-place or blue/green.

For Amazon ECS and AWS Lambda there are three ways traffic can be shifted during a deployment:

* Canary: Traffic is shifted in two increments. You can choose from predefined canary options that specify the percentage of traffic shifted to your updated Amazon ECS task set / Lambda function in the first increment and the interval, in minutes, before the remaining traffic is shifted in the second increment.
* Linear: Traffic is shifted in equal increments with an equal number of minutes between each increment. You can choose from predefined linear options that specify the percentage of traffic shifted in each increment and the number of minutes between each increment.
* All-at-once: All traffic is shifted from the original Amazon ECS task set /  Lambda function to the updated Amazon ECS task set / Lambda function all at once.

## Architecture Patterns - deployment and management
* global company needs to centrally manage creation of infrastructure services to accounts in AWS organizations => centralization (= organization, service catalog, ...)
  * define infra in CloudFormation
  * create service catalog products and portfolios in central account
  * share using Organizations
* company is concerned about malicious attacks on RDP and SSH ports for remote access to EC2: use System Manager with the SSM agent (session manager)
* development team requires method of deploying applications using CloudFormation. Developers typically use JavaScript and TypeScript: define resources in JavaScript and TypeScript and use Cloud Development Kit to create CloudFormation templates
* need to automate the process of updating an application when code is updated: create a CodePipeline that sources code from CodeCommit and use CodeBuild and CodeDeploy
* need to safely deploy updates to EC2 through a CodePipeline. Resources defined in CF templates and app code stored in S3: use CodeBuild to automate testing, use CF changes set to evaluate changes and CodeDeploy to deploy using a blue/green deployment pattern
* company currently uses Chef cookbooks to manage infrastructure and is moving to the cloud. Need to minimize migration complexity: OpsWorks (Chef Automate)

## Components

**Deployment group**: 
* deploys a revision to a set of instances
* belong to one application and specifies
  * deployment config: deployment rules, success/failure condition used during a deployment
  * notifications configuration for deployment events
  * CloudWatch alarms to monitor a deployment
  * Deployment rollback configuration

* Environment Configuration: we need to define the environment configuration like ASG, EC2 instances, on-premises instances, load balancer. Basically, this must match our environment where the application will be deployed.

* Deployment settings: how fast an application will be deployed and the success or failure conditions for a deployment. Default is **AllAtOnce, OneAtATime, HalfAtATime.**

**Deployment**: deploys a new version that consists of an application and AppSpec file

* need to specify where the revision type is (S3, GitHub)
* each region will have a different URL: https://s3.amazonaws.com/aws-codedeploy-us-east-1/samples/latest/sample.zip => content + appspec file

**Deployment Configuration**: settings that determine the deployment speed and the minimum number of instances that must be healthy at any point during a deployment

**Revision**: a combination of an AppSpec file and application files, such as executables, configuration files and so on

**Application**: a collection of deployment groups and revisions.

**Compute platform**: where the application will be deployed; can be EC2/on-prem, ECS, Lambda

## Pre-requisites

1. provision IAM user with the rights to have impact on the système (ASG, EC2, Lambda, ECS, S3, some specific IAM permissions)
2. install or upgrade and then configure AWS CLI.
3. create a service role for AWS CodeDeploy (depends on the type of deployment we want like ECS vs Lambda vs EC2 vs on-prem) => **the IAM user has all required access, the service role has less access because it is specific to a single deployment kind**. 
4. create an IAM instance profile for the EC2 instances
5. in the user data of the EC2: install CodeDeploy resources kit
   1. curl -O https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install && chmod +x ./install && ./install auto

## Deployment types

**In-place deployment**

* existing servers are updated with the new version of the application
* application on each instance in the deployment group is stopped, the latest app revision is installed and the new version of the application is started and validated
* will always be this deployment for the first version of the app since we don't have any other
* not great if the app is critical, prefer Blue/Green 

**Blue/Green deployment (EC2)**

* new application versions are deployed on a new set of instances
* traffic is routed from old to new instances
* if there are failures, the application can fall back to the older deployment version
* **we need to specify the new application name, deployment group name, asg name, load balancer name, service role name and a key pair if we want EC2 access -> this should not conflict with what exists**
* on EC2/on-prem: instances in a deployment group (the original env) are replaced by a different set of instances. What to install from S3/GitHub, what lifecycle event hooks to run in response to deployment lifecycle events
* Lambda: traffic is shifted from current serverless environment to one with the updated Lambda function version. Which functions to deploy, which functions to us for validation.
* ECS: traffic is shifted from the task set with the original version of a containerized application in an ECS service to a replacement task set in the same service. The protocol and port of a specified load balancer listener is used to reroute production traffic. During a deployment, a test listener can be used to serve traffic to the replacement task set while validation tests are run.

**Blue/Green deployment (Lambda)**

* traffic is shifted from one Lambda version to another, this can happen in multiple ways
  * **Canary**:
    * a percentage of traffic is shifted to the new version
    * CodeDeploy then waits for a specified time and shifts the rest of the traffic if it sees no errors
  * **Linear**:
    * traffic is shifted in equal increments with an equal number of minutes between each increment
  * **All at once**
    * traffic is immediately and completely shifted to the new version of the Lambda function
    
## AppSpec.yml

- available hooks depend on the deployment type

- hooks allow arbitrary scripts to run during deployment process

- typical example include:

  - BeforeInstall
  - AfterInstall
  - ApplicationStart
  - ApplicationStop
  - ValidationService

  =>  param for all location of the scripts, timeout, runas

```yaml
version: 0.0
os: linux
files:
	- source: /
	  destination: /var/www/html/WordProcess
hooks:
	BeforeInstall:
		- location: scripts/install_depdencies.sh
		  timeout: 300
		  runas: root
	AfterInstall:
		- location: scripts/change_permissions.sh
		  timeout: 300
		  runas: root
	ApplicationStart:
		- location: scripts/start_server.sh
		- location: scripts/create_test_db.sh
		  timeout: 300
		  runas: root
	ApplicationStop:
		- location: scripts/stop_server.sh
		  timeout: 300
		  runas: root
```

hooks are a set of instructions to be run to deploy the new version (hooks have timeouts).

