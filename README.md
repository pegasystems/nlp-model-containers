## Table of contents
* [General info](#general-info)
* [Machine Learning NLP container](#machine-learning-nlp-container)
* [Deep Learning NLP container](#deep-learning-nlp-container)

## General info
This is an example dockerized container which comes with the dependencies required to run your machine learning and deep learning models

This uses flask to serve the models using a rest end point secured with Authlib for OAuth2 (using https://docs.authlib.org/en/latest/flask/2/) as well as 
an end point without auth.

<b>Notes:</b> Please note that it is <b><u>not for</u></b> production use cases as this has an un authenticated endpoint and also it doesn't run on SSL

The Repo contains 2 containers.
* Machine Learning Container
* Deep Learning Container

Please find the steps to be followed:

* Step1: Train The Model
* Step2: Save the Train,Vectorizer model
* Step3: Dump the saved model into specific location(nlp-model-containers/machine-learning-nlp-container/models/)
* Step4: Initialize the Flask API via Docker container
* Step5: Predict and access the endpoints


## Machine Learning NLP container
<i>The project contains:</i>
* README.md
* Dockerfile
* requirments.txt
* app.py
* sample training scripts(nlp-model-containers/machine-learning-nlp-container/samples/)
* sample saved models(nlp-model-containers/machine-learning-nlp-container/models/)

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
* sample training scripts(nlp-model-containers/deep-learning-nlp-container/samples/)
* sample saved models(nlp-model-containers/deep-learning-nlp-container/models/)

<i>Algorithm Supported(Keras Framework):</i>
* Tensorflow
* Microsoft Cognitive Toolkit (CNTK)
* Theano
