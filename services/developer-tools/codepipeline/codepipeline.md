# AWS CodePipeline

## General Info

before Continuous Integration -> integration hell when multi dev. The longer before the integration, the more chances we have to have issues when reintegrating.

CI -> automating regular code commits followed by automated build and test process designed to highlight integration issues early (the smaller the change, the less time it took to make it -> less likely to have big impact)

Need new tooling -> Jenkins, GoCD, TeamCity, ...
Potential high resources requirements on big project

CI/CD service that can be used through AWS CodeStar or through the AWS Console for fast and reliable applicatino and infra updates. CodePipeline builds, tests and deploys the code every time there is a code changed based on the release process models we define.

**Used for automating the release process. CodeBuild is only used to create artifacts and run unit tests. CodePipeline will deploy app on staging environments and run additional tests like performance tests, ...**

Source stage can accept inputs from GitHub, AWS CodeCommit or S3.

Directly integrates with CodeDeploy, OpsWorks and BeanStalk, can also deploy container-based applications to services by using AWS ECS.

Tooling integrations
* Source stage: S3, CodeCommit, Github, ECR, Bitbucket Cloud (beta)
* Build: CodeBuild, Jenkins
* Deploy: CloudFormation, CodeDeploy, ECS, Beanstalk, AWS Service Catalog, S3

Also supports Lambda:

* changes env with CloudFormation
* create resources at a stage and delete them at another
* swap CNAME values to achieve zero downtime
* deploy to ECS
* backup resources before building or deploying by creating an AMI snapshot
* notification (slack, IRC, ...)

For manual actions, if nobody approves the action before 7 days, it is considered a failure.

We can select CloudFormation (create, delete stack) as a deployment action in any stage of our pipeline.

Benefits of CodePipeline

* automate release processes - source repository through build, test and deploy
* consistent release process - define the set of steps before new changes are released
* real time status of the process - view alerts, retry actions, manually rerun any pipelines
* tooling integrations for
  * source control: S3, CodeCommit, GitHub => **changes are detected using CloudWatch for CloudCommit**
  * Build: CodeBuild, CloudBeens, Jenkins, TeamCity, SolanoCI
  * Test: CodeBuild, HOE StormRunner, Load BlazeMeter, Nouvola, Runscope, Ghost Inspector
  * Deploy: CloudFormation, CodeDeploy, ECS, Beanstalk, OpsWorks, XebiaLabs

Pipeline needs an IAM role with the correct permissions to function properly.

The pipeline can be updated after its creation to add new stages and so on.

Pay as you go

**CodePipeline zips and transfers the files for input or output artifacts as appropriate for the action type in the stage.**

**A S3 bucket is central to everything, bucket is per region: source output artifacts, build input artifacts, build output artifacts, deploy input artifacts, ...**

When we run code pipeline, the S3 bucket **MUST** have versioning enabled.

**When we want to deploy on EC2 instances, the EC2 instances must be tagged since CodeDeploy can use up to 3 tags to know on which instances it will install the software through CodeDeploy.**

**CodePipeline needs a service role that can be created automatically when creating the pipeline.**

The recommended "change detection" option is CloudWatch events but can we CodePipeline (periodic checks).

**Source and deploy steps are mandatory, build is optional.**

can get notified whenever there is a pipeline, stage, or action status change in AWS CodePipeline

Notifications when there is a pipeline, stage, or actions status change in CodePipeline. CodePipeline is integrated with CloudWatch events (detect and react to changes in the state of a pipeline, a stage or an action. Then based on rules we create, CloudWatch events invokes one or more target actions) and we can receive notifications with SNS or invoke an AWS Lambda function on a status change.

CodePipeline can work with CodeCommit, GitHub, ...

CodePipeline can orchestrate a pipeline, we need CodeBuild to do stuff (build, test, ...)

* Source stage – S3, CodeCommit, Github, ECR, Bitbucket Cloud (beta).
* Build – CodeBuild, Jenkins.
* Deploy stage – CloudFormation, CodeDeploy, ECS, Elastic Beanstalk, AWS Service Catalog, S3.

## Concepts

**Pipelines**: workflow that describes how software changes go through release processes

**Artifacts**: 
* files or changes that will be worked on by the actions and stages in the pipeline
* each pipeline stage can create artifacts
* artifacts are passed, stored in S3 and then passed on to the next stage

**Artifact Store** 
* bucket in the same region as the pipeline to store items for all pipelines in that region associated with our account. 
* Every time we use the console to create another pipeline in that region, AWS CodePipeline creates a folder for that pipeline in the bucket. 
* It uses that folder to store artifacts for our pipeline as the automated release process runs.

**Stages**: 
* pipelines are broken up into stages like build stage, test stage (jenkins test, ...), deploy stage. 
* Stages use input and output artifacts that are stored in the artifact store for our pipeline
* each stage can have sequential actions and/or parallel actions
* can define manual approval step 
* Valid stages are:
  * source: s3, CodeCommit, Github, ECR
  * build: CodeBuild, Custom Jenkins or other CI
  * test: CodeBuild, Custom Jenkins or others
  * deploy: S3, CloudFormation, CodeDeploy, ECS, Beanstalk, OpsWorks, Alexia, ...
  * approval: Manual approval before next stage, 7 days timeout
  * invoke: Lambda

**Actions**: 
* stages contain at least one action
* these actions take some action on artifacts and will have artifacts as either an input, an output or both
  * **Approval (manual after SNS topic warning), Source, Build, Test, Deploy, Invoke**. 
* If we add cross-region action to our pipeline, we provide an artifact bucket for each region where we have actions.

**Transitions**: progressing from one stage to another inside of a pipeline

