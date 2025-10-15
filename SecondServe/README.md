# SecondServe

## Requirements

To properly run SecondServe locally the following programs must be installed
1. Docker
2. Python 3.13
3. MongoDB Community Server (https://www.mongodb.com/try/download/community)
4. Node.js (Manages the Angular package setup)

Before running the SecondServe application, create a copy of "env.template" file and name it ".env"
This will be the enviroment variables file for your project, do not push this file to the repo, as it contains
information that is private and only relevant to your machine. The only required field that must be updated is the DJANGO_SECRET_KEY.

The DJANGO_SECRET_KEY can be generated through the use of the generateKey.py program. This program will generate
a secretKey and print it to the command line. Keys should be kept private and not shared or pushed to a repo.

## Execution

To run SecondServe navigate to the SecondServe Directory then execute
```sh
docker compose up --build
```

If something goes wonky, you can remove the created containers by using
```sh
docker compose down -v
```

## Project Structure
```
SecondServe/
├─ docker-compose.yml      # Docker configurations for running the project
├─ env.template
├─ .env                    # Local environment Variables
├─ README.md
├─ backend/                # The Django Project (handles Backend and Database functions)
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ manage.py
│  └─ SecondServe/
│     ├─ __init__.py
│     ├─ settings.py
│     ├─ urls.py
│     └─ wsgi.py
└─ frontend/               # The Angular Project (handles Frontend functions)
   ├─ Dockerfile
   ├─ nginx.conf           # NGINX Config -> Routes backend calls through/from frontend
   ├─ proxy.conf.json      # dev proxy to backend
   └─ web/                 # Angular workspace
```
