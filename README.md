# Task Manager CLI

## About The Project

This project consists of basic python end points made in python using Fast API as part of a course assignment with access token and session auth implemented.

## Getting Started

This section will guide you through setting up your project locally. To get a local copy up and running, follow these simple steps.

### Installation

1.  Clone the repo
    ```bash
    git clone git@github.com:mFahadYounas/FastAPI_with_Auth.git
    ```
    If you already have a version of the repo, make sure to get the latest version by pulling from the above repo
2.  Navigate into the project directory
    ```bash
    cd FastAPI_with_Auth
    ```
3.  Make a .env file with the following environment variables
    ```bash
    POSTGRES_USER=your postgres database user name here
    POSTGRES_PWD=your postgres password here
    POSTGRES_URL=db:5432
    DB_NAME=any db name you would like to give your postgres db
    REDIS_URL=redis://redis:6379/0
    JWT_SECRET_KEY=your JWT secret key here
    ```

## Usage

1. Run the application by using the following command:

```bash
docker compose up
```

2. Open localhost:8000/docs to try out the APIs