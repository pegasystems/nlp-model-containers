# Deploy custom python Deep learning models

This is an example dockerized container which comes with the dependencies required to run your Deep learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as an end point without auth

## Prerequisites
    1. Docker installed

## Train and Save Deep Learning model

Sample script of training the ML model is available in `nlp-model-containers/deep-learning-nlp-container/samples/` folder. The training script contains example of creating `*h5*` file.
##### Saved models
    1. tokenization pkl file
    2. Enocer pkl file
    3. Model Hyper Parameter yaml file
    4. Model Wweights H5 file

Users can refer the sample scripts and modify the scripts w.r.t requirments.

Users can train DL model using Keras Framework(can be customized to use tensorflow/CNTK/theano as a backend)

## Take a quick look
This is a ready to run example 

##### 1)Create the docker image
    $ docker build --tag <REPOSITORY_NAME>:<TAG> .
<b>Notes</b>:    
    create and tag the docker image using the Dockerfile defined in the project. 
    execute the above command in the location where you have `requirments.txt` and `dockerfile`
    
##### 2)Run the docker
    $ docker run -e PYTHONUNBUFFERED=1 --publish <PORT-MAPPING>:<PORT-MAPPING> --detach --name [container_name]<REPOSITORY_NAME>:<TAG>

##### 3)View the Docker Container and the logs
    $ docker ps
    $ docker logs -f [container_name]
   
##### 4)Predict
    The end point to predict with authentication is `/auth/predict`
    The end point to predict without authentication is `/noauth/predict`
    
This uses `OAuth 2.0 `

Following are the endpoint available

/login : Use this endpoint to login any any username - currently any user is accepted as valid - once the user is created, use 'create client' option to create authentication credentials - ensure you select grant_types with "client_credentials" - Use the generated client secret and password to use auth endpoint


##### Additional Information
for Deep Learning Model, modelIdentifier would be name of the folder which contains artifacts(h5,pkl,yaml,etc..) in the models folder.
(`nlp-model-containers/deep-learning-nlp-container/models/keras_small_talk_model/`)

(Example if the keras with tensorflow as a backend model is saved as keras_small_talk_model.pkl  then the `modelIdentifier` would be `keras_small_talk_model`)
