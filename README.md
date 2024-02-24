[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB)](https://docs.python.org/3/whatsnew/3.11.html)
[![FastApi](https://img.shields.io/badge/framework-fastapi-009688)](https://fastapi.tiangolo.com/ko/)
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

# Fastapi + Dependency_Injector + Redis + Postgresql + celery Base Project Template

<!--
- [Fastapi + Redis + Postgresql + Dependency_Injector Base Project Template](#Fastapi + Redis + Postgresql + Dependency_Injector Base Project Template)
  - [특징](#특징)
  - [빌드](#빌드)
    - [1. .env에 환경변수 세팅](#1-env에-환경변수-세팅)
    - [2. docker-compose 실행](#2-docker-compose-실행)
    - [3. fastapi앱 컨테이너 접속하여 마이그레이션 실행](#3-fastapi앱-컨테이너-접속하여-마이그레이션-실행)
  - [웹요청 동작확인](#웹요청-동작확인-(Postman-사용))
    - [1. .env에 환경변수 세팅](#1-env에-환경변수-세팅)
    - [2. docker-compose 실행](#2-docker-compose-실행)
    - [3. fastapi앱 컨테이너 접속하여 마이그레이션 실행](#3-fastapi앱-컨테이너-접속하여-마이그레이션-실행)
    - [4. 백그라운드(celery)로 뉴스게시글 등록(3개의 게시글이 등록됨)](4-백그라운드(celery)로-뉴스게시글-등록(3개의-게시글이-등록됨))
    - [5. 뉴스리스트 조회)](5-뉴스리스트-조회)
  - [OpenApi 로도 요청가능](OpenApi로도-요청가능)
  -->

## 특징

- [x] **SQLAlchemy 2.0 only**를 사용하여 최상의 비동기 쿼리지원 (SQLAlchemy 2.0.0 was released January 26, 2023)
- [x] Postgresql database `asyncpg` 라이브러리 사용
- [x] [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations
- [x] [Dependency_Injector](https://python-dependency-injector.ets-labs.org/) 라이브러리를 사용하여 DI전략 구현
- [x] [starlette middleware](https://www.starlette.io/middleware/#basehttpmiddleware) 의 dispatch를 통해 미들웨어 클래스를 구현
- [x] jwt를 통한 사용자 인증
- [x] celery, celery-beat 사용을위한 메세지 브로커로 redis를 사용하여 백그라운드 작업 및 스케줄러 작업 구현
- [x] dockerfile 과 docker-compose.yml 를 통한 빌드
- [x] docker 빌드시 web서버로 nginx, WSGI로 gunicorn, ASGI로 uvicorn 사용
- [x] [Poetry](https://python-poetry.org/docs/) 사용하여 인터프리터 관리 용이
- [x] pytest 비동기 테스트 (fake-redis 사용)

## 빌드

### 1. .env에 환경변수 세팅
루트에있는 env.example을 .env로 변경후 알맞게 세팅해준다. (아래 예제참고) </br>
<b>주의할점은 DB_HOST와 REDIS_HOST는 docker-compose에 노드네임으로 설정해줘야한다.</b>
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

### 2. docker-compose 실행
빌드를위해 아래명령어 실행후 nginx, fastapi, redis, postgresql, celery, celery-beat 컨테이너 실행확인
```
docker-compose up --build
```
컨테이너 조회 docker ps
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/45c9acc4-9e7b-45d2-be39-a0c08087ec61)



### 3. fastapi앱 컨테이너 접속하여 마이그레이션 실행
docker exec -it '컨테이너명' /bin/bash 로 해당 노드접속후 /app경로에서 아래 alembic 명령어 실행
```
alembic upgrade head 
```
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/493c26e8-350f-4d31-8f58-7b003d15fea9)


## 웹요청 동작확인 (Postman 사용)

### 1. 사용자 등록
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/3776dc5f-6cdb-4348-9ca4-6582ea7ebf1f)


### 2. 로그인
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/73a60b73-e311-4517-95b0-4d1ab99e82c8)


### 3. 뉴스게시글 등록
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/01adfc4f-069f-49bc-b6ac-285266990a6e)


### 4. 백그라운드(celery)로 뉴스게시글 등록(3개의 게시글이 등록됨)
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/6e463ffd-6703-47d5-856e-16ab9aa1b0ec)

celery worker가 메세지 브로커(redis)에 쌓인 task 가져가서 실행
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/1b53b4e2-9584-4d96-939e-77c9a96f0f6e)


### 5. 뉴스리스트 조회
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/91d9d97f-b41c-4bb4-a362-1e49752db38d)


## OpenApi 로도 요청가능
Swagger (http://127.0.0.1:8080/api/v1/docs)
![image](https://github.com/CHOJUNGHO96/Fastapi-dependency_injector-Redis-Postgresql-docker-ProjectTemplate/assets/61762674/becd03e6-dc4c-400b-ba44-89e349af6b11)





