 ## Simple flask persona_api

 ## Run server
 Python version == 3.8.6

 ### Using Docker
 ```shell
 #clone the repo
 $ docker built -t persona_api ./
 $ docker run -d --name apiserver -p 5000:5000 persona_api:latest
 ```

 ### Using virtual env
 ```shell
 #clone the repo
 $ cd /path/to/the/repo
 $ python3 -m venv flask
 $ source flask/bin/activate
 $ pip install -r requirements.txt
 $ python src/main.py
 ```

 ### Testing
 ```shell
 $ cd /path/to/the/repo
 $ python3 -m venv flask
 $ source flask/bin/activate
 $ pip install -r requirements.txt
 $ pytest
 ```

### Endpoint testing using swagger

By entering http://127.0.0.1:5000/apidoc you can see the swagger UI for basic testing