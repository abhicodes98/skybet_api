from flask import Flask, jsonify, request
import psycopg2
import shortuuid
from dotenv import load_dotenv

import os, re
from datetime import datetime



if os.getenv('ENV','dev') == 'dev':
    load_dotenv()

class Config:
    APP_NAME = os.getenv('APP_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

if not Config.APP_NAME:
    raise ValueError("APP_NAME is required")

app = Flask(Config.APP_NAME)
app.config.from_object(Config)
app.json.sort_keys = False

# This function will create a connection to the database
def create_db_connection():
    return psycopg2.connect(
        dbname=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        host=app.config['DB_HOST']
    )


# this function will be called before every request
@app.before_request
def middleware():
    path = request.path 
    if 'localhost' in request.url:
        return

    if 'get-token' not in path:
        user = UserDetail()
        token = request.args.get('token')
        res = {'status': "failed", 'message': "Token is Required"}
        if not token:
            return jsonify(res), 400
        if not user.token_verify(token):
            res['message'] = "Token is Invalid"
            return jsonify(res), 400


# This function will be called after every request
@app.after_request
def middleware_after_request(response):
    if 'localhost' in request.url or 'get-token' in request.path:
        return response

    if response.status_code == 200:
        user = UserDetail()
        token = request.args.get('token')
        user.increment_api_count(token)
    
    if response.content_type == 'application/json':
        data = response.get_json()
        status = data.get('status')
        try:
            int(status)
        except:
            status = str(status).title()
            data['status'] = status
        msg = data.get('message')
        if msg:
            msg = str(msg).title()
            data['message'] = msg
        
        response = jsonify(data)
        return response
    
    else:
        # create a new json response
        res = {
            'status': "ERROR",
            'message': "Internal Server Error"
        }
        response = jsonify(res)
        response.status_code = 500
        return response
        


def email_validation(email):
    valid_re = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(valid_re.match(email))

class UserDetail:
    appname = app.config['APP_NAME'].title()
    token_type = "paid"
    api_count = 0
    is_brevo = False

    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        with create_db_connection() as conn:
            self.conn = conn
            self.cur = conn.cursor()

    def search_email(self, email):
        try:
            self.cur.execute(
                "SELECT token FROM account_userdetail WHERE email = %s and appname = %s", 
                             (email, self.appname)
                             
                            )
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error in search_email: {e}")
            return None

    def get_token(self):
        return str(shortuuid.random(10))

    def create_user(self, email):
        created_at = datetime.now()
        token = self.get_token()
        try:
            self.cur.execute(
                "INSERT INTO account_userdetail (email, token, appname, token_type, api_count, is_brevo, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (email, token,
                 self.appname,
                 self.token_type,
                 self.api_count,
                 self.is_brevo,
                 created_at,
                 created_at,
                 )
            )
            self.conn.commit()
            return token
        except Exception as e:
            print(f"Error in create_user: {e}")
            return None

    def get_user_token(self, email):
        token = self.search_email(email)
        if token:
            return token, "old"
        
        return self.create_user(email), "new"

    def token_verify(self, token):
        try:
            self.cur.execute("SELECT * FROM account_userdetail WHERE token=%s;", (token,))
            count = self.cur.fetchone()
            return bool(count)
        except Exception as e:
            print(f"Error in token_verify: {e}")
            return False

    def increment_api_count(self, token):
        try:
            self.cur.execute("UPDATE account_userdetail SET api_count=api_count+1  WHERE token=%s;", (token,))
            self.conn.commit()
        except Exception as e:
            print(f"Error in increment_api_count: {e}")


@app.route("/get-token", methods=['GET'])
def get_token():
    response_msg =  {'status': 400, 'message': 'Email is Required'}
    try:
        # Get the 'email' parameter from the query string
        email = request.args.get('email')
        if not email:
            return jsonify(response_msg), 400

        
        if not email_validation(email):
            response_msg['message'] = 'Check the email address you entered'
            return jsonify(response_msg), 400

        # Instantiate UserDetail class
        user = UserDetail()
        token, user_type = user.get_user_token(email)
        
        if 'invalid' in token.lower():
            response_msg['message'] = 'Invalid Email Address'
            return jsonify(response_msg), 400

        # Check if token is generated successfully
        if token:
            response_msg['status'] = 200
            msg = 'Token Generated Successfully' if user_type == "new" else 'Welcome Back'
            response_msg['message'] = msg
            response_msg['token'] = token
            return jsonify(response_msg), 200
    
    # Handle internal server error
    except Exception as e:
        print(f"Error in get_token: {e}")
        response_msg = {
            'status': 500,
            'message': 'Internal Server Error'
        }
        return jsonify(response_msg), 500


