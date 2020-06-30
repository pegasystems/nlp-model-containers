## Table of contents
* [General info](#general-info)
* [Machine Learning NLP container](#machine-learning-nlp-container)
* [Deep Learning NLP container](#deep-learning-nlp-container)

## General info
The Repo contains 2 containers.
* Machine Learning Container
* Deep Learning Container

Please find the steps to be followed:

* Step1: Train The Model
* Step2: Save the Train,Vectorizer model
* Step3: Initialize the Flask API via Docker container
* Step4: Predict and access the endpoints
	
## Machine Learning NLP container
The project contains:
* README.md
* Dockerfile
* requirments.txt
* app.py
* sample training scripts(nlp-model-containers/machine-learning-nlp-container/samples/)
* sample saved models(nlp-model-containers/machine-learning-nlp-container/models/)

Algorithm Supported(Scikit/SKlearn):
* Boosting Algos( XGBoost/LightBoost/AdaBoost/CatBoost)
* Decision Tree
* Random Forest
* Naive Bayes(Multionomial and Gausian)
* SVM
* KNN

## Deep Learning NLP container
The project contains:
* README.md
* Dockerfile
* requirments.txt
* app.py
* sample training scripts(nlp-model-containers/deep-learning-nlp-container/samples/)
* sample saved models(nlp-model-containers/deep-learning-nlp-container/models/)

Algorithm Supported(Keras Framework):
* Tensorflow
* Microsoft Cognitive Toolkit (CNTK)
* Theano
