# AWS DeepLens

## General info

fully programmable video camera, tutorials, code and pre-trained models designed to expand deep learning skills. 
The device has a GPU powerful enough to do visual based inference. We create a model on SageMaker and we deploy it
on the device using AWS GreenGrass.

There are a lot of pre trained models that we can directly put on the device.

The deeplens camera is linked to an account (=> registered). When we deploy a project, there is an web interface that 
allows us to see the results.

The video is not designed to be a real time live feed, there is a small delay.

The messaging format is MQTT (lightweight) desgiend for IoT.

Integrated with Rekognition, SageMaker, Polly, TensorFlow, MXNet, Caffe

deeplens outputs a Kinesis Video Streams

## Creation
Projects: definition of all the resources that the project will need

Models: the model name needs to start with "deeplens-" because of the service policy which restricts the access.
The models need to be as small as possible so we don't want the checkpoints normally created during the training job.
To deploy on deeplens, put the hyperparameter checkpoint_frequency equal to the number of epochs. This way we only do
one checkpoint at the end and the model is a few hundreds MB instead of GB.

Everything in deeplens is well integrated with sagemaker, we reference training job for the model and so on. We need to 
be aware of the model framework because deeplens will create a package with the runtime (mxnet, tf, ...) and the model.

The code executed on deeplens is lambda but a different kind. The lambda code is executed in a loop indefinitely and do not timeout on the deeplens device.
We still need to publish the lambda function because greengrass needs to reference a specific version.

## Deployment
need to reference the model, the lambda and create a deployment package.

This is done automatically with the console, we specify which model, which lambda and click deploy. Under the hood,
the runtime with the DL framework will be merged with the model and the lambda in a package that will then be deployed
to the deeplens device.

## IoT and MQTT
the device streams the lambda output to AWS IoT using MQTT. We can subscribe to that topic and see the changes in real time.

