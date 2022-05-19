# AWS Simple Workflow Service

## General Info

build, run and scale background jobs that have parallel or sequential steps => fully managed state tracker and task coordinator

if an application's steps take more than 500 milliseconds to complete, we need to track the state of processing

Coordinates and manages the execution of activities. It manages a specific job from start to finish while still allowing for distributed/decoupled architecture.

SWF make decisions based on a decider program that is written in the language of our choice.

Amazon SWF is used for processing background jobs that have parallel or sequential steps.

You can think of Amazon SWF as a fully managed state tracker and task coordinator.

Use Amazon SWF if your app’s steps take more than 500 milliseconds to complete, you need to track the state of processing, or you need to recover or retry if a task fails.

Best suited for human-enabled workflows like an order fulfilment system or for procedural requests.

SWF uses a task-oriented API.

SWF ensures a task is assigned once and never duplicated.

SWF keeps track of all the tasks and events in an application.


Essentials:

* SWF is fully managed workflow service provided by AWS
* allows an architect/developer to implement distributed, async applications as workflow
* a workflow coordinates and manages the executions of activities that can be run async across multiple computing devices
* consistent execution
* guarantees the order in which tasks are executed, guarantees delivery order of message/tasks
* there are no duplicate tasks
* SWF is primarly an API which an application can integrate its workflow into. THis allows the service to be used by non-AWS service, such as an on-premises data center
* workflow execution can last up to 1 year

**=> could potentially be used in Amazon: buy product, validate payment, prepare package (human), send to customer**

## Components

* **Workflows** (or decider): sequence of steps required to perform a specific tasks 
* **Domains**: scope of workflows, can have multiple workflows in a domain but workflows in different domains cannot communicate
* **Activities**: single step (or unit of work) in the workflow
* **Tasks**: what interacts with the workers that are part of a workflow, there are two kinds of tasks
  * **Activity task**: tells a worker to perform a function (encode video, check inventory, ...)
  * **Decision task**: tells the decider the state of the work flow execution, which allows the decider to determine the next activity to be performed
* **Workers**: responsible for receiving a task and taking action on it: can be any type of component such as an EC2 instance or even a person

## Comparison with other services

SWF and SQS

* similarities
  * both can be used to create distributed systems
  * both allow each task/component to scale independently
* differences
  * SWF can have a human task as part of the workflow
  * SWF workflows and tasks can last up to 1 year, SQS messages only live 14 days

SWF and step functions

* similarities
  * both can help create coordinating application components
* differences
  * SWF uses a decider program, not a JSON defined state machine to make decisions
  * SWF does not have the visual workflow of Step Functions
  * SWF gives us complete control over orchestration logic but increases the complexity of our applications
