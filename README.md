# BD

This is the repo of my comics' collection website!

It's a Django project that displays my collection of comics.

> Website available at address: [bd.h.minet.net](http://bd.h.minet.net)

## Table of Contents

- [App Structure](#app-structure)
- [Installation](#installation)
- [Deploy](#deploy)
- [Authors](#authors)

## App Structure

- [static/](bd/main/static): The files used by the website (images, documents, css & javascript…)
- [templates/](bd/main/templates): The html templates of the pages
- [views.py](bd/main/views.py): the code launch when loading a page
- [bd/](bd/bd): the settings files (urls, wsgi, settings) used by Django
- [manage.py](bd/manage.py): the main file that runs the website

## Installation

> You need to have python3 and pip installed on your machine

1. Clone git repository

    ```bash
    git clone git@github.com:juliette39/bd_website.git
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
   
5. Create the database

   ```bash
   python3 bd/main/update_database.py
   ```

6. Launch the website

    ```bash
    cd bd
    ./manage.py runserver 
    ```
7. To leave the virtual environment
    ```bash
    deactivate
    ```

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
    ServerName bd.h.minet.net
    ServerAdmin juliette.debono@telecom-sudparis.eu

    AddDefaultCharset UTF-8

    Alias /static /home/juliettedebono/bd_website/bd/main/static/
    <Directory /home/juliettedebono/bd_website/bd/main/static/>
        Require all granted
    </Directory>

    <Directory /home/juliettedebono/bd_website/bd/bd/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess bd_process python-home=/home/juliettedebono/bd_website/env python-path=/home/juliettedebono/bd_website/bd
    WSGIProcessGroup bd_process
    WSGIScriptAlias / /home/juliettedebono/bd_website/bd/bd/wsgi.py process-group=bd_process

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

- Juliette Debono
