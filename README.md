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
3. Run `pipenv install --dev` from the root folder of the repository.
You might have an error with psycopg2. In that case, remove its line from Pipfile, execute the command again and then run
`pipenv install psycopg2`.
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
    


## Google Cloud Platform deployment

### Requirements

All the local development requirements, plus:

- [gcloud SDK](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- If you need to expose a new endpoint or make changes to an existing one, you must redeploy the API definition
Swagger file. The swagger API definition files are under `devops/swagger`.


### Steps

#### 1. Docker image

1. Build the docker image. 
Given that your are in project's root folder:

    ```bash
    docker build -t carto_test_back .
    ```

2. Push the image to the registry:

    ```bash
    docker push <google cloud container>/carto_test_back:latest
    ```

    (You might need to get credentials first: `gcloud auth configure-docker`)

1. Set-up `gcloud` with your account credentials and select the project where you'll be deploying. Also, you need
to get authentication credentials for the cluster. 

Follow the [quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart).

#### 2. Kubernetes

1. You must generate the yaml deployment file from the template in 
`devops/deployment-template.yaml` with the configuration settings of the desired environment. For example, 
for `itg` environment:

    ```
    python3 generate_config.py -d devops --template deployment-template.yaml --config devops/config/itg-deployment.yaml deployment.yaml
    ```

1. Once you have generated the deployment file from the template, you apply it with:
    
    ```
    kubectl apply -f back-carto_test-deployment.yaml
    ```

1. To manually update the image in the deployment:
    
    ```
    kubectl set image deployment/esp-carto_test_back carto_test=gcr.io/<gcloud container name>/carto_test_back:latest
    ```

    If the image has the same tag, yoy might need to patch the deployment instead:

    ```
    kubectl patch deployment esp-carto_test -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"date\":\"`date +'%s'`\"}}}}}"
    ```

#### 3. Google Endpoints and Swagger

[swagger](https://swagger.io/docs/) is used to define the API and [swagger-ui](https://swagger.io/tools/swagger-ui/) to
expose the documentation. The swagger files are under `devops/swagger`, you can use them right away in
swagger-ui to see and validate the definition. For convenience, there is a script in `devops/swagger-ui/swagger-server.sh`
that starts a swagger-ui Docker container serving those files. Google Endpoints, Google Cloud's API manager, 
supports OpenAPI 2.0 definition, but with some
 [limitations](https://cloud.google.com/endpoints/docs/openapi/openapi-limitations)).

**Notes on developing the Swagger definition:**

- Path definitions should be placed in `swagger-template.yaml`

- Each model definition should be in its own individual yaml file, under `models`. If some entity or endpoint has
several models, it is convenient to create a subfolder to group them all (for example, `models/air_quality`).

The Jenins/CI system automatically generates a deployable `swagger.yaml` file so that you do not have to worry about
doing so. 


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