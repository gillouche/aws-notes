# AWS CodeBuild

## General Info

Managed build service that can compile the source code, run unit tests and produce deployment artifacts **without** needing to provision, manage or scale build servers.

AWS CodeBuild is a fully managed continuous integration (CI) service that compiles source code, runs tests, and produces software packages that are ready to deploy.

Scales continuously and process multiple builds concurrently, pay as you go

Uses a file "**buildspec.yml**" that describes the (pre/post) build actions.

Benefits of CodeBuild

* fully managed by AWS
* on-demand: AWS scales with our needs
* pay on the time it takes to complete the builds
* pre-configured environments for many popular programming languages that contains
  * OS
  * programming language runtime
  * build tools (maven, gradle, npm)
* can use Docker images
* integrated with KMS encryption for build artifacts, IAM for build permissions, VPC for network security and CloudTrail for logging API calls

Source can be GitHub, CodeCommit, CodePipeline and S3

Can use CloudWatch alarms to detect failed builds and trigger SNS notifications

Builds can be defined with CodePipeline or CodeBuild itself

CodeBuild can be added as a build or test action to the build or test stage of a pipeline in CodePipeline

Provides prepackaged build environments for the most popular programming languages and build tools such as maven, gradle and more.

Can also customize build environments in AWS CodeBuild to use our own build tools

Can run CodeBuild by using the CodeBuild or CodePipeline console

Can automate the running of CodeBuild by using the AWS CLI or AWS SDKs.

Default timeout of a build is 1 hour and we cannot change that.

CloudWatch logs are optional but enabled by default (build logs) -> auto sent to cloudwatch logs, same as Alexa and Lambda


## Concepts

**Build project**: defines how CodeBuild will run a build and answers questions like

* where is the source code ? S3, CodeCommit, Bitbucket, Github, GithubEntreprise
* what build env to use ?
* what build commands to run?
* where to store the output of the build? S3 or no artifacts

**Build environment**: the OS (image, docker, ...), language runtime, tools that CodeBuild uses for the build, if we want a cache for the build. 
We need a service role (can be existing or a new one created by CodeBuild). 

**Build Spec**: a YAML file (buildspec.yml) that describes the collection of commands and settings for CodeBuild to run a build => similar to .gitlab-ci.yml

* env: create environment variables for the build
* phases: describes the phase of the build
  * install
  * pre_build
  * build
  * post_build
* artifacts: path of the created artifact
* cache: paths of the files to cache

* Preconfigured build environments: Java, Python, Node.JS, Ruby, Go, Android, .NET core for Linux and Docker
* Custom: Docker via DockerHub or Amazon ECR

## Process

1. as input, we must provide CodeBuild with a build project (GitHub, S3, CodeCommit, ...)
2. CodeBuild uses the build project to create the build environment
3. CodeBuild downloads the source code into the build environment and then uses the build specification (build spec), as defined in the build project or included directly in the source code
4. if there is any build output, the build environment uploads its output to an S3 bucket
5. while the build is running, the build environment sends information to CodeBuild and CloudWatch logs
6. can get summarized info from CodeBuild and CloudWatch

## Buildspec.yml

Must be at the root of the source code

Nothing can happen without a buildspec.yml file. The formatting needs to be correct otherwise we will have errors during the build.

If the code is on S3, it needs to be a zip file (or folder) containing a certain directory hierarchy.

We cannot add more phases or change the name.

Artifacts section will end up in S3 (+ cache for future builds).

```yaml
version: 0.2

phases:
	install:
		commands:
			- echo "Nothing to do in the install phase..."
    pre_build:
    	commands:
    		- echo "Nothing to do in the pre_build phase..."
   build:
   		commands:
   			- echo "Build started on `date`"
   			- mvn install
   post_build:
		commands:
			- echo "Build complete on `date`"
artifacts:
	files:
		- target/messageUtil-1.0.jar
```

Can define environment variables (plaintext or secure secrets via SSM parameter store)

We can also use CodeBuild locally using Docker and the CodeBuild agent (debugging purposes).