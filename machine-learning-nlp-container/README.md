# Deploy custom python machine learning models

This is an example dockerized container which comes with the dependencies required to run your deep learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as an end point without auth

## Prerequisites
    1. Docker installed

## Take a quick look
This is a ready to run example 

Create the docker image
    # create and tag the docker image using the Dockerfile defined in the project
    $ docker build --tag <REPOSITORY_NAME>:<TAG> .

Run the docker 
    $ docker run -e PYTHONUNBUFFERED=1 --publish <PORT-MAPPING>:<PORT-MAPPING>  --detach --name [container_name]<REPOSITORY_NAME>:<TAG>

Predict
    The end point to predict with authentication is /auth/predict
    The end point to predict with authentication is /noauth/predict

This uses OAuth 2.0 

Following are the endpoint available

/login : Use this endpoint to login any any username - currently any user is accepted as valid - once the user is created, use 'create client' option to create authentication credentials - ensure you select grant_types with "client_credentials" - Use the generated client secret and password to use auth endpoint