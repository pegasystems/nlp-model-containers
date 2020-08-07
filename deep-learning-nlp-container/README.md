# Deploy custom python Deep learning models

This is an example dockerized container which comes with the dependencies required to run your Deep learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as an end point without auth

## Prerequisites
    1. Docker installed

## Train and Save Deep Learning model

* Sample script of training the ML model is available in `nlp-model-containers/deep-learning-nlp-container/samples/` folder. 
* The training script contains example of creating `*h5*` file.

##### Saved models
    1. tokenization pkl file
    2. Encoder pkl file
    3. Model Hyper Parameter yaml file
    4. Model weights H5 file

* `Tokenization pkl file:`  The main purpose of this file is to vectorize the text corpus, by turning each text into vector where the coefficient for each token could be based on tf-idf.
* `Encoder pkl file:` The main purpose of this file is to convert the label encoded category to original category
* `Model Hyper Parameter file:` The main purpose of this file is to configure hidden layers, neurons, activation function required by the Neural Network.
* `Model weights file:` The main purpose of this file is to save the configurations specified in the model hyper parameter file and then to use them during inference.

Users can refer the sample scripts and modify the scripts w.r.t requirments.

Users can train DL model using Keras Framework(can be customized to use tensorflow/CNTK/theano as a backend)

## Build and Run Container
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
   
## Access model through REST API

* Service discovery endpoint (Open API) :<br>
`/api/docs` : The service discovery endpoint based on swagger open API standard. This can be used while creating the custom model service instance in pega.

* Model Endpoint API:<br>
`/auth/predict` - Use this endpoint for prediction with authentication. parameters are specified below<br>
`/noauth/predict` - Use this endpoint for prediction without authentication. parameters are specified below

* parameters:<br>
  `modelIdentifier` - Identifier of the model to use for evaluation<br>
  `text` - Text to be analysed.

* Additional Info:<br>
  modelIdentifier would be name of the folder which contains artifacts(h5,pkl,yaml,etc..) in the models folder.(`nlp-model-containers/deep-learning-nlp-container/models/keras_small_talk_model/`)<br><br>
 (Example if the artifacts of keras with tensorflow is saved in folder `keras_small_talk_model`  then the `modelIdentifier` would be `keras_small_talk_model`)

    
## List of other API:

`/login` : Use this endpoint to login any any username - currently any user is accepted as valid - once the user is created, use 'create client' option to create authentication credentials - ensure you select grant_types with <b>"client_credentials"</b> - Use the generated client secret and password to use auth endpoint

`/noauth/predict`: Use this endpoint for prediction without authentication. details reagrding modelIdentifier is mentioned in Additional Information section

`/auth/predict`: Use this endpoint for prediction with authentication. details reagrding modelIdentifier is mentioned in Additional Information section

`/oauth/token` : OAuth 2 token generation endpoint used to create the tokens. This is used to get the refresehed tokens. 

`/oauth/revoke` : OAuth 2 revoke endpoint.

The endpoints `/oauth/token` and `/oauth/revoke` is used for authentication rule in pega along with the client id and client secret. They are required only during authenticated endpoint(`/auth/predict`)

