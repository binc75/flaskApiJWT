#!/usr/bin/env python3

#
#
# RestAPI with Authentication & JWT
#
#

from flask import Flask, request, jsonify, make_response
import datetime
import jwt
import json


# Initialize Flask app
app = Flask(__name__)
app.config['PRESHARED_SECRET_KEY'] = 'arbitrary secret key used to encode/decode/sign jwt'


# Initialize user DB (read from json file)
with open('userdb.json') as f:
    userdb = json.load(f)


# Routes
@app.route('/public', methods=['GET'])
def get_public_page():
    return jsonify({'message': 'You reached a public page!'})


@app.route('/private', methods=['GET'])
def get_private_page():

    token = None

    # Check if token is passed in the header of the request, if the case set token to this value
    # Checking for "x-access-token" or "Authorization: Bearer"
    print(request.headers)
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace('Bearer ', '')

    # If token is not provided return 401
    if not token:
        return jsonify({'message': 'Authentication token is missing!'}), 401

    # Check token validity 
    try:
        token_data = jwt.decode(token, app.config['PRESHARED_SECRET_KEY'])
        user_from_token = token_data['username']
        exp_date_from_token = datetime.datetime.fromtimestamp(token_data['exp']).strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'message': '{}, you reached a private page'.format(user_from_token),'token_valid_until': '{}'.format(exp_date_from_token)}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token is expired!'}), 403

    except:
        return jsonify({'message': 'Token provided is not valid'}), 401


@app.route('/login')
def login():

    # Gather request informations about authentication
    auth = request.authorization

    # If the object auth is missing then pop up request for authentication
    if not auth or not auth.username or not auth.password:
        return make_response('Can not verify identity. Unauthorized!', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # Check username & password
    if auth.username in userdb and auth.password == userdb[auth.username]['password']:
        token = jwt.encode({'username': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['PRESHARED_SECRET_KEY'])
        print(token.decode('UTF-8'))
        return jsonify({'token': token.decode('UTF-8')}), 200
    else:
        return jsonify({'message': 'Username or password incorrect!'}), 401

    return jsonify({'message': 'Unauthorized!'}), 401


# Initialize main app
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080', debug=True)
