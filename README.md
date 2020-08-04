## Table of contents
* [General info](#general-info)
* [Machine Learning NLP container](#machine-learning-nlp-container)
* [Deep Learning NLP container](#deep-learning-nlp-container)

## General info
This is an example dockerized container which comes with the dependencies required to run your machine learning and deep learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as 
an end point without auth.


<b>Notes:</b> Please note that it is a <b><u>sample</u></b> Docker Container. scripts can be modified and deployed with/without authentication.

The Repo contains 2 containers.
* Machine Learning Container
* Deep Learning Container

Please find the steps to be followed:

* Step1: Train the model
* Step2: Save the model
* Step3: Dump the saved model into specific location
* Step4: Initialize the Flask API via Docker container
* Step5: Predict and access the endpoints

<b>Note:</b> Detailed steps are available in the Machine Learning and Deep Learning respective README.md files

Machine Learning:
https://github.com/pegasystems/nlp-model-containers/tree/master/deep-learning-nlp-container

Deep Learning:
https://github.com/pegasystems/nlp-model-containers/tree/master/machine-learning-nlp-container


## Machine Learning NLP container
<i>The project contains:</i>
* README.md
* Dockerfile
* requirments.txt
* app.py
* sample training scripts(https://github.com/pegasystems/nlp-model-containers/tree/master/machine-learning-nlp-container/samples)
* sample saved models(https://github.com/pegasystems/nlp-model-containers/tree/master/machine-learning-nlp-container/models)

<i>Algorithm Supported(Scikit/SKlearn):</i>
* Boosting Algos( XGBoost/LightBoost/AdaBoost/CatBoost)
* Decision Tree
* Random Forest
* Naive Bayes(Multionomial and Gausian)
* SVM
* KNN

## Deep Learning NLP container
<i>The project contains:</i>
* README.md
* Dockerfile
* requirments.txt
* app.py
* sample training scripts(https://github.com/pegasystems/nlp-model-containers/tree/master/deep-learning-nlp-container/samples)
* sample saved models(https://github.com/pegasystems/nlp-model-containers/tree/master/deep-learning-nlp-container/models/keras_small_talk_model)

<i>Algorithm Supported(Keras Framework):</i>
* Tensorflow
* Microsoft Cognitive Toolkit (CNTK)
* Theano
