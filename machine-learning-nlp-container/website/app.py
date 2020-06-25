#Generic Packages
import os
import time
import pandas as pd
import numpy as np
import pickle
np.random.seed(1337)

#Flask Packages
from flask import Flask
from flask_restplus import Api, Resource, fields
from flask import request, session, url_for
from flask import render_template, redirect, jsonify, make_response


#Authentication Packages
from .oauth2 import config_oauth
from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from .models import db, User, OAuth2Client
from .oauth2 import authorization, require_oauth

#logger
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
import logging
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logger = logging.getLogger(__name__)

def create_app(config=None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object('website.settings')

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    setup_app(app)
    return app


def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    config_oauth(app)


flask_app = create_app({
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
})

def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

app = Api(app = flask_app, 
          version = "1.0", 
          title = "Text analysis", 
          description = "Natural language processing",
          doc="/doc")


name_space = app.namespace('', description='NLP Prediction service')

data_model = app.model('Parameters', 
                  {'modelIdentifier': fields.String(required = True, 
                                         description="Identifier of the model to use for evaluation", 
                                         help="Model identifier cannot be empty"),
                    'text': fields.String(required = True, 
                                         description="Text to be analyzed", 
                                         help="Text cannot be empty")
                  })

headers = {'Content-Type': 'text/html'}
models_cache = {}

def mlPredict():
    try:
        data = request.get_json()
        testdata = data['text']
        modelName = data['modelIdentifier']
        testdataL = str(testdata).split(';')

        directory = "./models"

        ####loading the saved pkl file ##############
        modelFile = os.path.join(directory, modelName + "." + 'pkl');
        model = None
        try:
            model = models_cache[modelFile]
        except KeyError as e:
            with open(os.path.join(directory, modelName + "." + 'pkl'), "rb") as f:
                model = pickle.load(f)
                models_cache[modelFile] = model

        logger.debug("######### model info####################")
        logger.debug(model)
        logger.debug("#########model loaded succesfully########")

        ################## Prediction################
        prediction = pd.DataFrame(model.predict(testdataL))
        confidenceScore = model.predict_proba(testdataL)

        ################## Confidence Score #####################
        confidenceScore = confidenceScore[0][np.argmax(confidenceScore)]
        confidenceScore = pd.DataFrame(pd.Series(confidenceScore))

        ################## Attribute Names##################
        prediction.rename(columns={0: "label"}, inplace=True)
        confidenceScore.rename(columns={0: "score"}, inplace=True)

        ###################### Json Output ####################
        confScrore = str(round(confidenceScore['score'][0], 2))

        logger.debug('')
        logger.debug('')
        logger.debug('#############Metrics######################')
        logger.debug('Input Text:' + testdata)
        logger.debug('Prediction:' + prediction['label'][0])
        logger.debug('Algorithm:' + modelName)
        logger.debug('Predicted Class:' + prediction['label'][0])
        logger.debug('Confidence Score:' + confScrore)
        logger.debug('###################################')

    except KeyError as e:
        name_space.abort(500, e.__doc__, status="Error Accessing Keys", statusCode="500")
    except Exception as e:
        name_space.abort(400, e.__doc__, status="Unknown Error", statusCode="400")

    return testdata, prediction, confScrore

##########################################################################################
#Scikit Learn ML - Without Authentication
##########################################################################################

@name_space.route("/noauth/predict")
class PredictClass(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={})
    @app.expect(data_model)
    def post(self):
        print("noauth")
        testdata,prediction,confScrore = mlPredict()
        return jsonify(text=testdata,
                       topic={'name': prediction['label'][0],
                              'score': confScrore})

##########################################################################################
#Scikit Learn ML - With Authentication
##########################################################################################

@name_space.route("/auth/predict")
class PredictClass(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={})
    @app.expect(data_model)
    @require_oauth('profile')
    def post(self):
        print("auth")
        testdata, prediction, confScrore = mlPredict()
        return jsonify(text=testdata,
                       topic={'name': prediction['label'][0],
                              'score': confScrore})

@name_space.route("/login")
class LoginPage(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def get(self):
        try: 
            user = current_user()
            if user:
                clients = OAuth2Client.query.filter_by(user_id=user.id).all()
            else:
                clients = []
            return make_response(render_template('home.html', user=user, clients=clients),200,headers)
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
    def post(self):
        headers = {'Content-Type': 'text/html'}
        try:
            username = request.form.get('username')
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username)
                db.session.add(user)
                db.session.commit()
            session['id'] = user.id
            return redirect('/login')
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")



@name_space.route("/logout")
class LogoutAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def get(self):
        headers = {'Content-Type': 'text/html'}
        try:
            del session['id']
            return redirect('/login')
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")


@name_space.route("/create_client")
class CreateClientAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def get(self):
        try:
            user = current_user()
            if not user:
                return redirect('/login')
            if request.method == 'GET':
                return make_response(render_template('create_client.html'),200,headers)
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
    def post(self):
        try:
            headers = {'Content-Type': 'text/html'}
            user = current_user()
            if not user:
                return redirect('/login')
            
            client_id = gen_salt(24)
            client_id_issued_at = int(time.time())
            client = OAuth2Client(
                client_id=client_id,
                client_id_issued_at=client_id_issued_at,
                user_id=user.id,
            )

            if client.token_endpoint_auth_method == 'none':
                client.client_secret = ''
            else:
                client.client_secret = gen_salt(48)

            form = request.form
            client_metadata = {
                "client_name": form["client_name"],
                "client_uri": form["client_uri"],
                "grant_types": split_by_crlf(form["grant_type"]),
                "redirect_uris": split_by_crlf(form["redirect_uri"]),
                "response_types": split_by_crlf(form["response_type"]),
                "scope": form["scope"],
                "token_endpoint_auth_method": form["token_endpoint_auth_method"]
            }
            client.set_client_metadata(client_metadata)
            db.session.add(client)
            db.session.commit()
            return redirect('/login')
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")

@name_space.route("/oauth/authorize")
class OAuth2AuthorizeAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def get(self):
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return make_response(render_template('authorize.html', user=user, grant=grant),200,headers)
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def post(self):
        try:
            if not user and 'username' in request.form:
                username = request.form.get('username')
                user = User.query.filter_by(username=username).first()
            if request.form['confirm']:
                grant_user = user
            else:
                grant_user = None
            return authorization.create_authorization_response(grant_user=grant_user)
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")


@name_space.route("/oauth/token")
class IssueTokenAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def post(self):
        try:
            print("Getting auth tokens")
            return authorization.create_token_response()
        except KeyError as e:
            print(e)
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            print(e)
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")


@name_space.route("/oauth/revoke")
class RevokeTokenAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    def post(self):
        try:
            return authorization.create_endpoint_response('revocation')
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")

@name_space.route("/api/me")
class ApiMeAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={})
    @require_oauth('profile')
    def get(self):
        try:
            user = current_token.user
            return jsonify(id=user.id, username=user.username)
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")

@name_space.route("/api/docs")
class ApiDocsAction(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={})
    def get(self):
        try:
            return redirect(url_for('specs'))
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
