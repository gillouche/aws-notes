# AWS DeepRacer

## General info
1/18th scale race car to get started with reinforcement learning; learns very complex behaviors without requiring any labeled training data and can 
make short term decisions while optimizing for a longer term goal

learn through autonomous driving, can get started with virtual car and tracks in cloud-based 3D racing simulator

can deploy trained models onto AWS DeepRacer and race other people or take part in the global AWS DeepRacer League

Use the same camera than deeplens with our model inside the car to move along a track.

We don't need the physical car, we can just play virtually.

## Creation
1. Create account resources (IAM roles, a valid AWS DeepRacer resources stack)
2. learn the basics of reinforcement learning
    * no training data
    * we just provide an action space that the model can do (move left, right, ..)
    * we provide feedback during the training (good or bad) based on actions
3. the action space defines all the actions that the car can take both in virtual and physical world
    * maximum steering angle in degrees
    * steering angle granularity
    * maximum speed in m/s
    * speed granularity
4. generate the action list with all the possibilities defined in the action space. The format is something like
action number (0), steering (-30 degrees), speed (0.5m/s) and so on. The bigger the list, the longer the training.
5. define the reward function (python script) that take the inputs of the scene and return the reward as float. This function is evaluated
each time the car choses an action.
6. choose hyperparameters 
7. stop conditions: timeout for the training

The training job will trigger AWS robomaker (specialized sagemaker for robot making) to handle the training.
This is not really a training job but a simulation job.

We still don't want to overfit because if anything at all is different in the real environment, the car won't be able to do anything.