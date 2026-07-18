# Codexio

This is the repo of my comics' collection website!

It's a Django project that displays my collection of comics.

> Website available at address: [codexio.julsql.fr](http://codexio.julsql.fr)

## Table of Contents

- [App Structure](#app-structure)
- [Installation](#installation)
- [Deploy](#deploy)
- [Authors](#authors)

## App Structure

- [static/](src/main/static): The files used by the website (images, documents, css & javascript…)
- [templates/](src/main/templates): The main html templates
- [core/](src/main/core): The core of the project, using an hexagonal architecture:
    - application: Application use cases (business logic orchestration)
    - domain: Domain layer: models, business rules, interfaces
    - infrastructure: Adapters for APIs, database, file system, views
- [clean_data](src/main/clean_data): The script to clean the data
- [src/](src/config): the settings files (urls, wsgi, settings) used by Django
- [manage.py](src/manage.py): the main file that runs the website

## Docker

You can run the docker-compose.yml and access to the website:

```bash
docker-compose -f docker-compose-local.yml up --build 
```

And access to localhost:8000

To shut down:

```bash
docker-compose -f docker-compose-local.yml down
```

## Test

Run tests in `src/`

`./src/manage.py test ./src/tests`

## Installation

> You need to have python3 and pip installed on your machine

1. Clone git repository

    ```bash
    git clone git@github.com:julsql/codexio.git
    ```

2. Don't forget to add the .env file in `./src/config/.env` and the Google sheet api keys file at
   `./src/config/google-project.json`. You will need to create a new project in Google could console, and enable the API:
- Google Drive API
- Google Sheets API

Think to give access to the client_email in your sheet.

    ```bash
    SECRET_KEY='django-key'
    DEBUG=False
    POST_TOKEN="TOKEN"
    GSHEET_CREDENTIALS='config/google-project.json'
    ```

3. Configure the python virtual environment

    ```bash
    pip install virtualenv
    cd codexio
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the libraries

    ```bash
    pip install -r requirements.txt
   ```

5. Creation of the privates files

    ```bash
    cd src/
    
    nano config/.env
    nano config/google-project.json
    mkdir database
    chmod -R 755 database/
    sudo chown -R www-data:www-data database/
    mkdir media/main/images/dedicaces
    mkdir media/main/images/exlibris
    chmod -R 755 media/
    sudo chown -R www-data:www-data media/
    ```

6. Create the database

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

7. Launch the website

    ```bash
    ./manage.py runserver
    ```

8. To leave the virtual environment
    ```bash
    deactivate
    ```

### Upload photo

You can upload image with a `POST` request
The body request a form sending a file with key `file`.

The urls are:

- http://codexio.julsql.fr/upload/dedicace/isbn/ for the dedicace
- http://codexio.julsql.fr/upload/exlibris/isbn/ for the ex-libris

## Deploy

Deployment is fully automated and runs on k3s.

1. On every push to `main`, the [`docker.yml`](.github/workflows/docker.yml) CI
   workflow builds the Docker image and pushes it to GitHub Container Registry
   (GHCR).
2. On the k3s cluster, [Keel](https://keel.sh) polls GHCR and detects the new
   image digest, then triggers a rolling update of the deployment automatically.

The Kubernetes manifests (deployment, service, ingress…) live in the
[`k3s-manifests`](https://github.com/julsql/k3s-manifests) repository. There is
nothing to do by hand: merge to `main` and Keel rolls out the new image.

## Authors

- Jul SQL
