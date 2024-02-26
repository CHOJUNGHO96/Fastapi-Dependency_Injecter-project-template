[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB)](https://docs.python.org/3/whatsnew/3.11.html)
[![FastApi](https://img.shields.io/badge/framework-fastapi-009688)](https://fastapi.tiangolo.com/)
[![dependency injector](https://img.shields.io/badge/DependencyInjector-blue)](https://python-dependency-injector.ets-labs.org/)
[![Postgresql](https://img.shields.io/badge/Postgresql-15-4169E1)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-DC382D)](https://redis.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00)](https://www.sqlalchemy.org/)
[![jwt](https://img.shields.io/badge/authentication-jwt-black)](https://jwt.io/)
[![Black](https://img.shields.io/badge/code%20style-black-lightgrey)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/code%20style-isort-lightgrey)](https://pycqa.github.io/isort/)
[![pytest](https://img.shields.io/badge/pytest-passing-0A9EDC)]([https://github.com/psf/pytest](https://docs.pytest.org/en/8.0.x/))
[![docker](https://img.shields.io/badge/docker-2496ED)](https://www.docker.com/)
[![nginx](https://img.shields.io/badge/web-nginx-009639)](https://www.nginx.com/)
[![gunicorn](https://img.shields.io/badge/WSGI-gunicorn-499848)](https://gunicorn.org/)
[![uvicorn](https://img.shields.io/badge/ASGI-uvicorn-40AEF0)](https://www.uvicorn.org/)
[![alembic](https://img.shields.io/badge/migration-alembic-83B81A)](https://alembic.sqlalchemy.org/en/latest/)
[![poetry](https://img.shields.io/badge/interpreter-poetry-60A5FA)](https://python-poetry.org/)

# Fastapi + Dependency_Injector + Redis + Postgresql + Celery Base Project Template

## Directory structure
```
├─app
│  ├─apis
│  │  └─v1
│  │      ├─auth
│  │      │  ├─login
│  │      │  │  ├─repositories
│  │      │  │  └─service
│  │      │  ├─logout
│  │      │  ├─refresh_token
│  │      │  │  ├─repositories
│  │      │  │  └─service
│  │      │  ├─registration
│  │      │  │  ├─repositories
│  │      │  │  └─service
│  │      ├─background
│  │      │  └─news_crawling
│  │      └─news
│  │          └─list
│  │              ├─repositories
│  │              └─service
│  ├─celery_task
│  │  └─job
│  ├─common
│  ├─database
│  │  └─schema
│  ├─errors
│  ├─middlewares
│  ├─models
│  └─util
├─migrations
│  └─versions
├─nginx
└─scripts
```


## Features

- [x] **SQLAlchemy 2.0 only** for optimal asynchronous query support (Released January 26, 2023)
- [x] Postgresql database with `asyncpg` library
- [x] [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations
- [x] Implementing DI strategy using [Dependency_Injector](https://python-dependency-injector.ets-labs.org/) library
- [x] Middleware class implementation through dispatch in [starlette middleware](https://www.starlette.io/middleware/#basehttpmiddleware)
- [x] User authentication via JWT
- [x] Background tasks and scheduler jobs using Redis as the message broker for celery, celery-beat
- [x] Building with dockerfile and docker-compose.yml
- [x] Using nginx as web server, gunicorn for WSGI, and uvicorn for ASGI in docker build
- [x] Easy interpreter management with [Poetry](https://python-poetry.org/docs/)
- [x] Asynchronous tests with pytest (using fake-redis)
- [x] All endpoint responses are unified to [fastapi JSONResponse](https://fastapi.tiangolo.com/advanced/response-directly/#using-the-jsonable_encoder-in-a-response)
- [x] [pre-commit](https://pre-commit.com/) with poetry export and ruff

## Build

### 1. Setting Environment Variables in .env
Change the root env.example to .env and set appropriately. (Refer to the example below) </br>
<b>Attention: DB_HOST and REDIS_HOST should be set as node names in docker-compose.</b>
```
JWT_ALGORITHM=HS256
JWT_ACCESS_SECRET_KEY=SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_SECRET_KEY=SECRET_KEY
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=10080
DB_POOL_RECYCLE=1800
DB_HOST=postgres
DB_PORT=5432
DB_USER=DB_USER
DB_PASSWORD=DB_PASSWORD
DB_NAME=DB_NAME
REDIS_PORT=6379
REDIS_HOST=redis
REDIS_PASSWORD=REDIS_PASSWORD
REDIS_EXPIRE_TIME=604800
RABBITMQ_HOST=127.0.0.1
RABBITMQ_ID=admin
RABBITMQ_PASSWORD=RABBITMQ_PASSWORD
RABBITMQ_PORT=5672
```

### 2. Executing docker-compose
Execute the command below for build and check the running containers for nginx, fastapi, redis, postgresql, celery, celery-beat
```
docker-compose up --build
```
Container query with docker ps
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/45c9acc4-9e7b-45d2-be39-a0c08087ec61)



### 3. Running Migrations in FastAPI App Container
Access the node with `docker exec -it 'container name' /bin/bash` and execute the following alembic command in /app path
```
alembic upgrade head 
```
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/493c26e8-350f-4d31-8f58-7b003d15fea9)


## Web Request Testing (Using Postman)

### 1. Registering a User
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/3776dc5f-6cdb-4348-9ca4-6582ea7ebf1f)


### 2. Login
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/73a60b73-e311-4517-95b0-4d1ab99e82c8)


### 3. Posting News Articles
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/01adfc4f-069f-49bc-b6ac-285266990a6e)


### 4. Background Posting of News Articles with Celery (3 Articles Posted)
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/6e463ffd-6703-47d5-856e-16ab9aa1b0ec)

Celery worker takes tasks queued in the message broker (redis) and executes them
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/1b53b4e2-9584-4d96-939e-77c9a96f0f6e)


### 5. Viewing News List
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/91d9d97f-b41c-4bb4-a362-1e49752db38d)


## Also Requestable via OpenApi
Swagger (http://127.0.0.1:8080/api/v1/docs)
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/becd03e6-dc4c-400b-ba44-89e349af6b11)





