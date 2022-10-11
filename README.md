# About

Hello, This is test project for TopTal by **Mate Bersenadze**.

Test project is about **Quiz API**.

To say it shortly, Users can create Quizzes, other users can play it and gain scores.

# API Demonstration video
![Video](https://toptal-test-bucket-mate.s3.eu-central-1.amazonaws.com/Screen+Recording+2022-10-10+at+23.23.37.mov)

## Technologies

Python version: **3.10.4**

For RESTful application newly created Web Framework: [FastAPI](https://github.com/tiangolo/fastapi)
by [Tiangolo](https://tiangolo.com/)

For Database: [PostgreSQL](https://www.postgresql.org/)

For Migrations: [Alembic](https://alembic.sqlalchemy.org/en/latest/)

For Code Formatting: [Black](https://github.com/psf/black) and [Flake8](https://flake8.pycqa.org/en/latest/) backed
by [Pre-Commit](https://pre-commit.com/)

To run PostgreSQL I am using docker containers locally.

# Guide to run API

## Create and Activate Virtual Environment

> Python 3.10 is **REQUIRED** to run application

Create virtualenv named venv
```shell
virtualenv venv --python=python3.10
```

Activate environment
```shell
source venv/bin/activate
```

## Install Requirements

First, to run application we need to install all the requirements.

Execute in Terminal

```shell
pip install -r requirements.txt
```

## Run PostgreSQL Database

You can also use already ready created PostgreSQL DB, but in this step we gonna run fresh empty DB.

You will need to have [Docker](https://www.docker.com/) engine installed and running.

To run DB execute this in terminal

```shell
docker run --name toptal-quiz-postgres -e POSTGRES_PASSWORD=toptal -p 5432:5432 -d postgres
```

This will run postgres DB on port **5432** with **user: postgres** and **password: toptal**
You can configure password or port that is being used.

## Create Environment File .env

Applications requires Environment variables. **DB_URI** and **SECRET_KEY**

1. **DB_URI** is being used to connect to our created DB.
2. **SECRET_KEY** is being used for jwt encode and decodings during authentication.

SECRET_KEY can be generated using this command

```shell
openssl rand -hex 32
```

Example **.env** File

```text
DB_URI=postgresql://postgres:toptal@localhost:5432/postgres
SECRET_KEY=040ce4734a42f6fe46b6b54925aa2383fa88f08c04bbf3e1f18b2e9fca0213d8
```

## Run Migrations

After you have successfully created and run PostgreSQL DB now you have to create all required tables. For this we can
use Alembic which was already installed in the previous step.

Just execute in terminal

```shell
alembic upgrade head
```

## and finally: Run the server

```shell
uvicorn server:app --port 8000
```

> **Running server like this on production is not recommended**

## API Documentation

We can see our API Documentation in Redoc or Swagger style
> Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
> Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
