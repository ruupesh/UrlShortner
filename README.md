Check redis connectivity:
python manage.py check_redis_connection   

check db connectivity:
python manage.py check_db_connection

Create docker build backend:
docker build -t url_shortner_backend .

Create docker build frontend:
docker build -t url_shortner_frontend .

Run docker container in interactive mode:
docker run -it -p 8000:8000 -e DJANGO_ENV=production url_shortner_backend /bin/bash

Run manage.py in docker container (from interactive mode):
python manage.py runserver 0.0.0.0:8000


Run docker container in detached mode backend:
docker run -d -p 8000:8000 url_shortner_backend

Run docker container in detached mode frontend:
docker run -d -p 80:80 url_shortner_frontend

Run docker container in detached mode with env variables:
docker run -d -p 8000:8000 -e DJANGO_ENV=production url_shortner_backend
