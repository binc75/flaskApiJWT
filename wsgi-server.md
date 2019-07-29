# wsgi server

For serve flask application with a productional web server you must to use uwsgi for execute requests to flask.

## prerequisites

- non-root user in sudores file
- domain pointing the machine
- ubuntu 18.04 LTS

## install packages

Install all the packages required for run `flaskApiJWT` on a webserver.

```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv
```

## create venv

Create venv for `flaskApiJWT` and download dependencies.

Before create the venv clone the repository, and go in his directory

```
cd ~
git clone https://github.com/binc75/flaskApiJWT.git
cd flaskApiJWT
```

Create venv and activate it:

```
python3.6 -m venv flaskApiJWT
source flaskApiJWT/bin/activate
```

Your command line will look like this:

```
(flaskApiJWT)user@host:~/$

```

Then install the requirements, wheel and flask

```
pip install -r requirements.txt
pip install wheel flask
```
## open firewall port for test

Open firewall port for test, port `8080`:

```
sudo ufw allow 8080
```

Run the test with: 

```
python flaskApiJWT.py
```

Now open your browser and inser the address `http://ip:8080/public`.

## Create wsgi entry point

Create the file `wsgi.py` in the root directory of the project.

```
vi ~/flaskApiJWT/wsgi.py
```

And write in the file:

```
from flaskApiJWT import app

if __name__ == "__main__":
	app.run()
```

Then test if it works correctly:

```
uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app
```

Now reopen your browser and insert the address `http://ip:8080/public`.

Then deactivate venv:

```
deactivate
```

## uWSGI config file

Create uWSGI config file in project root directory:

```
vi ~/flaskApiJWT/flaskApiJWT.ini
```

And write inside this code:

```
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = flaskApiJWT.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

## wsgi service

Create the service for wsgi for the project flaskApiJWT, create the file:

```
vi /etc/systemd/system/flaskApiJWT.service
```

And write inside the code bellow:

```
[Unit]
Description=uWSGI instance to serve flaskApiJWT
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/flaskApiJWT
Environment="PATH=/home/user/flaskApiJWT/flaskApiJWT/bin"
ExecStart=/home/user/flaskApiJWT/flaskApiJWT/bin/uwsgi --ini flaskApiJWT.ini

[Install]
WantedBy=multi-user.target
```

Start the service and enable it:

```
sudo systemctl start flaskApiJWT
sudo systemctl enable flaskApiJWT
sudo systemctl status flaskApiJWT
```

## Create nginx virtual server

Create the virtual server config file:

```
sudo vi /etc/nginx/sites-available/flaskApiJWT
```

And write in the file:

```
server {
    listen 80;
    server_name your.domain www.your.domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/user/flaskApiJWT/flaskApiJWT.sock;
    }
}
```

Enable the virtual server;

```
sudo ln -s /etc/nginx/sites-available/flaskApiJWT /etc/nginx/sitest-enalbed
```

Test nginx config

```
sudo nginx -t
```

If everything is ok restart nginx

```
sudo systemctl restart nginx
```

## adapt firewall

Remove test role and allow nginx:

```
sudo ufw delete allow 8080
sudo ufw allow 'Nginx Full'
```

Check if everithing is ok in your browser, open the link `http://your.domain/public`
