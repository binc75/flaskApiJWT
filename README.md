# Flask RestAPI POC

Simple RestAPI POC with authentication capabilities and JWT (JSON Web Token) management.

## Installation
``` bash
git clone https://github.com/binc75/flaskApiJWT.git
cd flaskApiJWT/
pip install -r requirements.txt
./flaskApiJWT.py
```
## Usage
Get a public page:
``` bash
curl -i http://127.0.0.1:8080/public

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/0.15.5 Python/3.7.1
Date: Fri, 26 Jul 2019 11:44:18 GMT

{
  "message": "You reached a public page"
  }

```

Authenticate with username / password and get a token
``` bash
$ curl -i --user nbianchi:12345 http://127.0.0.1:8080/login

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 153
Server: Werkzeug/0.15.5 Python/3.7.1
Date: Fri, 26 Jul 2019 11:42:29 GMT

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5iaWFuY2hpIiwiZXhwIjoxNTY0MTQzMTQ5fQ.q2xZWEL_za1tzWaUqZ7A8tS86HgvMy4JNZzTjdIkaIA"
  }


```

Access private page using the authorization token
``` bash
$ curl -i -H 'Accept: application/json' \
          -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5iaWFuY2hpIiwiZXhwIjoxNTY0MTQzMTQ5fQ.q2xZWEL_za1tzWaUqZ7A8tS86HgvMy4JNZzTjdIkaIA' http://127.0.0.1:8080/private

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 103
Server: Werkzeug/0.15.5 Python/3.7.1
Date: Fri, 26 Jul 2019 11:46:22 GMT

{
  "message": "nbianchi, you reached a private page", 
    "token_valid_until": "2019-07-26 14:12:29"
    }

```
