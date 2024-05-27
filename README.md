# integrate

## Overview

This is an insurance rating application. It allows user configuration of products, benefits, factors/relativities, and rates. Typically, these tasks would be done by back-office staff. Then, it allows users to generate custom quotes.

## Getting started

Clone the repo first.

```
git clone https://github.com/cmsommerville/integrate.git
cd integrate
```

Before building the application, you should configure environment variables. Copy `.env.template` to `.env`.

```
cp .env.template .env
```

Edit the `.env` file to set stronger passwords. Then run the application.

```
docker-compose up --build
```

This command will launch six services:

- `api`: this is the API layer, which is a Flask + SQLAlchemy application
- `db`: this is the database layer, which is MS SQL Server
- `redis`: this layer has several uses, including session storage/management, caching, Celery broker, and rate limiting management
- `celery_worker`: this is a Celery worker for background tasks
- `celery_beat`: this is a job scheduler
- `celery_dashboard`: this is a flower dashboard for monitoring Celery jobs

On launch, all services connect to each other with the usernames and passwords configured during setup. However, the database needs application tables. You need to run database migrations.

```
docker exec -it api sh -c "flask db upgrade"
```

In addition to creating all required database objects, this will initialize a sys admin user with the password you set in configuration. You should login with this user to start a session and add data to the database via API requests. The user name is `sys` and the password is whatever you set in configuration.

## Front end

There is a front end React application that is incomplete. Right now, it can be launched with this command:

```
cd frontend
npm install
npm run dev
```
