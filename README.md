# CARTO Tech Test

[![Python 3.7](https://img.shields.io/badge/python-3.7.4-blue.svg)](https://www.python.org/downloads/release/python-374/)
[![Django 3.1](https://img.shields.io/badge/Django-3.1-green.svg)](https://www.djangoproject.com/download/)
[![Pipenv](https://img.shields.io/badge/Pipenv-2020%2B-red.svg)](https://pipenv.readthedocs.io/en/latest/basics/)


## Local development

### Requirements

- [Python3.7](https://docs.python.org/3.7/)
- [pip3](https://pip.pypa.io/en/latest/installing/)
- Either [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/), 
or [PostgreSQL](https://www.postgresql.org/) and [PostGIS](https://postgis.net/) 


### Setup

1. Clone the repository
2. Install pipenv: `pip3 install pipenv`    
3. Run `pipenv install --dev` from the root folder of the repository
4. Run `pipenv run git-hooks` to auto install `pre-commit` and `pre-push` git hooks
5. Set the environment variable `DJANGO_READ_DOT_ENV_FILE=true`
6. Check that you have 2 files in `.envs/local`
  
    6.1. `.vars`: Configuration variables. The vars file should contain all variables declared
    in `config/settings/_vars.py`
    
    6.2. `.secrets`: Ask for it to get the latest version. The secrets file should contain all variables declared
    in `config/settings/_secrets.py`

#### Extra considerations

1. Database: If you chose to run PostgreSQL in Docker, you are all set. In case you run PostgreSQL in your local machine, 
you have to create a user and database and put its credentials in `local.py` and `test.py` settings files 
under `/config/settings`. 

2. Perhaps you need to install some geospatial libraries to allow the GeoDataBase to setup:

    `sudo apt-get install binutils libproj-dev gdal-bin`

### Available pipenv commands

- `pipenv run git-hooks [remove]`: Install [remove] `pre-commit` and `pre-push` git hooks
- `pipenv run linter`: Run the linter (uses [flake8](https://github.com/PyCQA/flake8))
- `pipenv run sort-imports`: Auto sort imports (uses [isort](https://github.com/timothycrosley/isort))
- `pipenv run test`: Run tests using `manage.py` and 4 parallel processes
- `pipenv run pytest`: Run tests using pytest


### Local deployment

1. Start PostgreSQL. You can run a script to start a postgres Docker container (with no persistent volume):  
`start_db.sh` located at `devops/db/postgres` (Don't forget to activate your virtual env!): 
`./devops/db/postgres/start_db.sh` ( ⚠️: an error on the first time could be normal, 
just relaunch the script a second time and. 
In case the script keeps failing, execute once with `sudo` and then again without it).

2. Run the django server:
    - The application is configured through environment variables, which for convenience should be specified in .env files. 
    For django to load them at start, set the environment variable `export DJANGO_READ_DOT_ENV_FILE=true`
    - Set the environment variable `export DJANGO_SETTINGS_MODULE=config.settings.local`
    - `python manage.py runserver 0.0.0.0:8000`


### Swagger
I've used [swagger](https://swagger.io/docs/) to define the API and [swagger-ui](https://swagger.io/tools/swagger-ui/) to
expose the documentation. The swagger files are under `devops/swagger`, you can use them right away in
swagger-ui to see and validate the definition. For convenience, there is a script in `devops/swagger-ui/swagger-server.sh`
that starts a swagger-ui Docker container serving those files. 


## Test and linter

You can make use of the available [pipenv commands](#available-pipenv-commands) or run 
any the following:

- Linter + tests + html coverage (The script by default activates the virtualenv generated with pipenv before running 
everything. This can be disabled with the flag `-no-venv`:
    ```
    ./run_tests.sh [--no-venv]
    ```

- Linter: 

    ```
    flake8 .
    ```

- Test:
    - with django manage.py test:

    ```
    python manage.py test carto_test --settings=config.settings.test
    ```

    - with pytest:
    ```
    pytest .
    ```
    
- Test with coverage: 

    ```
    coverage run manage.py test carto_test --settings=config.settings.test && coverage report
    ```
  In case you want an html report, add the following to the command above: `&& coverage html`