# Deploy custom python machine learning models

This is an example dockerized container which comes with the dependencies required to run your machine learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as an end point without auth

## Prerequisites
    1. Docker installed

## Train and Save Machine Learning model

Sample script of training the ML model is available in `nlp-model-containers/machine-learning-nlp-container/samples/` folder. The training script contains example of creating `*pkl*` file. users can modify the script to support `*joblib*` and `*bst*`.

Users can train ML model using various algorithm supported by scikit/sklearn library

The saved model should contain both vectorization process and the model details(example: provided in the training sample script)

## Take a quick look
This is a ready to run example 

##### 1)Create the docker image
    $ docker build --tag <REPOSITORY_NAME>:<TAG> .
<b>Note</b>: create and tag the docker image using the Dockerfile defined in the project

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
for Machine Learning Model, the modelIdentifier would be the "pkl" file name in the location ``nlp-model-containers/machine-learning-nlp-container/models/`
(Example if the Random Forest model is saved as smalltalk_model_randomforest.pkl. then the `modelIdentifier` would be `smalltalk_model_randomforest`


