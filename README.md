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

You need to configure your VM.

Don't forget to download git, python, apache2, pip on your VM:

```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install postgresql
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install git
sudo apt-get install python3-venv
```

After installing the project as explained in [Installation](#installation)
you can configure the VM as follows:

```bash
sudo nano /etc/apache2/sites-available/myconfig.conf
```

```
<VirtualHost *:80>
    ServerName url.domain.com
    ServerAdmin admin@email.fr

    AddDefaultCharset UTF-8

    Alias /static /home/username/codexio/src/main/static/
    <Directory /home/username/codexio/src/main/static/>
        Require all granted
    </Directory>

    <Directory /home/username/codexio/src/config/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess codexio_process python-home=/home/username/codexio/env python-path=/home/username/codexio/src
    WSGIProcessGroup codexio_process
    WSGIScriptAlias / /home/username/codexio/src/config/wsgi.py process-group=codexio_process

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

You load the configuration and restart the apache server

```bash
sudo a2ensite myconfig.conf
sudo service apache2 restart
```

> To unload a configuration: `sudo a2dissite myconfig.conf`

## Authors

- Jul SQL
