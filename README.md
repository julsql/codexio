# BD

This is the repo of my comics' collection website!

It's a Django project that displays my collection of comics.

> Website available at address: [bd.julsql.fr](http://bd.julsql.fr)

## Table of Contents

- [App Structure](#app-structure)
- [Installation](#installation)
- [Deploy](#deploy)
- [Authors](#authors)

## App Structure

- [static/](bd/main/static): The files used by the website (images, documents, css & javascript…)
- [templates/](bd/main/templates): The html templates of the pages
- [views.py](bd/main/views.py): the code launch when loading a page
- [bd/](bd/config): the settings files (urls, wsgi, settings) used by Django
- [manage.py](bd/manage.py): the main file that runs the website
- [upload.py](bd/main/upload_photo.py): the upload of photos of the ex libris or 'dedicace'

## Test

Run tests

`bd/manage.py test tests`

## Installation

> You need to have python3 and pip installed on your machine

1. Clone git repository

    ```bash
    git clone git@github.com:julsql/bd_website.git
    ```

2. Don't forget to add the settings file in `./bd/bd` and the google sheet api keys file at `private/bd-sheet-91.json`

3. Configure the python virtual environment

    ```bash
    pip install virtualenv
    cd bd_website
    python3 -m venv env
    source env/bin/activate
    ```
   
4. Install the libraries

    ```bash
    pip install -r requirements.txt
   ```

5. Creation of the privates files

    ```bash
    cd config
    mkdir db
    nano config/settings.py
    mkdir main/private
    nano main/private/config-sheet-91.json
    mkdir main/static/main/images/dedicaces
    mkdir main/static/main/images/exlibris
    chmod -R 755 main/static/main/images/exlibris
    sudo chown -R www-data:www-data main/static/main/images/exlibris/
    chmod -R 755 main/static/main/images/dedicaces
    sudo chown -R www-data:www-data main/static/main/images/dedicaces/
    ```
   
6. Create the database

   ```bash
    python3 main/update_database.py
    chmod -R 755 db/
    sudo chown -R www-data:www-data db/
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
      - http://bd.julsql.fr/upload/dedicace/isbn/ for the dedicace
      - http://bd.julsql.fr/upload/exlibris/isbn/ for the ex libris

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

    Alias /static /home/username/bd_website/bd/main/static/
    <Directory /home/username/bd_website/bd/main/static/>
        Require all granted
    </Directory>

    <Directory /home/username/bd_website/bd/bd/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess bd_process python-home=/home/username/bd_website/env python-path=/home/username/bd_website/bd
    WSGIProcessGroup bd_process
    WSGIScriptAlias / /home/username/bd_website/bd/bd/wsgi.py process-group=bd_process

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
