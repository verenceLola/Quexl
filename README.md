# Quexl

[![Build Status](https://travis-ci.com/verenceLola/Quexl.svg?token=A77sHzTptZ8EutExRXpa&branch=develop)](https://travis-ci.com/verenceLola/Quexl)
[![Build Status](https://verencelola.visualstudio.com/Quexl/_apis/build/status/verenceLola.Quexl?branchName=develop)](https://verencelola.visualstudio.com/Quexl/_build/latest?definitionId=12&branchName=develop)
![Build Status](https://github.com/verenceLola/Quexl/workflows/Django%20application/badge.svg)
[![codecov](https://codecov.io/gh/verenceLola/Quexl/branch/develop/graph/badge.svg?token=zNEszwcQ4u)](https://codecov.io/gh/verenceLola/Quexl)

This is an online marketplace for freelance services.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2acad8ef40948488fbab#?env%5BQuexl%5D=W3sia2V5IjoiYmFzZV91cmwiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoidG9rZW4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWV9XQ==)

The Application has been documented using Postman Documentation tht can be viewed [here.](https://documenter.getpostman.com/view/4146974/SVtVVp1U?version=latest)

## Setting Up the Application Locally

### Installing PostgreSQL

- PostgreSQL server is required by the application for the application to run. To use the local PostgreSQL server, ensure you have PostgreSQL [installed](https://www.postgresql.org/docs/12/tutorial-install.html) and running. ensure you add the server PostgreSQL connection URL to your .env file

    ``` bash
    DATABASE_URL=postgres://<user>:<password>@<host>:<port>/<database name> #  postgres://postgres@127.0.0.1:5432 if no username or password configured, or just a remote host's URL
    ```

### Setup VirtulEnvironment

- Setup Pyhton virtual environment by running `python3 -m venv venv`

- Activate the virtual environment by running `source venv/bin/activate`

### Install Application Dependencies

- Run the following command to install application dependencies `pip install -r requirements.txt`

- After installing the dependencies, add the necessary environmental variables required by the application. Sample environmental varials are:

    ```bash
    DEBUG=True
    DATABASE_URL=postgres://<user>:<password>@<host>:<port>/<database name>
    SECRET_KEY="611=df5*i4evgbpu3)$th%=##=kw#h#@8zomsn1$eo6f^uv74$" # sample SECRET_KEY
    ```

- Add the above variables in a file name `.env` in the root of the project

### Perform Initial Migrations

- To ensure that the database tables are properly configured, run migrations by running `./manage.py migrate` at the root of the project

### Start the Server

- After successfully performing migrations, the server can be started by running `./manage.py runserver` at the root of the project

### Running Tests

- To run unit test, [pytest](https://docs.pytest.org/en/latest/) is used. Run `pytest` at the root of the project

## Deployments and Releases

- The project had been deployed to Heroku. To view the various versions of the deployed apps, go [here](https://github.com/verenceLola/Quexl/deployments)
