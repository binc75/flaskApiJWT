## Python packets requirements
To generate the list of needed module I've used:
``` bash
$ pipreqs ./ --force
```
**IMPORTANT**: check that the bcrypt package is : ***bcrypt***
## Start with uWSGI web server (using venv)
```bash
git clone git@github.com:binc75/flaskApiJWT.git
cd flaskApiJWT/
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt --no-cache-dir
pip install uwsgi --no-cache-dir
uwsgi --http :8080  --callable app --processes 4 --threads 2 --wsgi-file flaskApiJWT.py 
```
