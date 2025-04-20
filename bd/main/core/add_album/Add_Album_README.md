# Bandes dessinées

## Introduction

Ce projet permet d'ajouter depuis son téléphone une bande dessinée à un gsheet.
S'il y a une erreur d'ajout dans le tableur, l'erreur est ajoutée dans le fichier [app.logs](bd/logs/app.logs).
Une fois l'ISBN ajouté, toutes les infos disponibles sur internet sont automatiquement ajoutées à un gsheet intitulé BD.

- Pour accéder au site web pour rechercher une bande dessinées : [bd.julsql.fr](http://bd.julsql.fr)
- Pour accéder au gsheet des bandes dessinées (si vous y avez
  l'accès) : [lien du gsheet](https://docs.google.com/spreadsheets/d/1z4iFF1ROr_sXZkkFJS12kKk7ndUaA9fNconarZIAIxo/edit?usp=sharing)

## Table des matières

- [Commandes](#commandes)
- [Structure](#structure)
- [Tests](#tests)
- [Configurations](#configurations)
- [Guide](#guide)
- [Auteur](#auteur)

## Commandes

Pour ajouter un album (-t & -l optionnels) :

```bash
python3 sheet_add_album.py 9782413043096 -t 0 -l "logs.txt"
```

Pour vérifier l'état des albums déjà renseignés et écrire dans le fichier log la trace d'execution (isbn & -l
optionnels)

```bash
python3 sheet_add_album.py 0 -t 1 -l "logs-test-gsheet.txt"
```

Il est aussi possible de convertir automatiquement toute la feuille de calcul en une base de données SQLite.
Pour cela :

```bash
python3 sheet_to_sql.py
```

### Quelques ISBN

> 9782413043096 # Saint-Elme\
> 9782864976165 # Astérix\
> 9782844148964 # Par toutatis !

## Structure

- [get_infos_bd.py](get_infos_bd.py) : Récupère à partir de l'ISBN les données sur la bande dessinées
- [sheet_add_album.py](sheet_add_album.py) : Script principal qui récupère les informations et les ajoute à la feuille
  de calcul
- [sheet_connection.py](sheet_connection.py) : Classe qui se gère la connection à la feuille de calcul
- [sheet_to_sql.py](sheet_to_sql.py) : Conversion de la feuille de calcul en base de données SQLite

## Tests

Il existe des tests [unitaires](../../tests/add_album/test_unit) et
d'[intégration](../../tests/add_album/test_integration).
Vous les trouverez dans le package [tests](../../../tests).

Pour tous les run :

```bash
python3 -m unittest discover tests
```

## Configurations

Configurer la VM

```bash
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
sudo apt install python3 -y
sudo apt install git
sudo apt-get update
sudo apt-get install python3-venv
sudo apt install python3-pip
pip install virtualenv
```

### Cloner git sur la VM

```bash
git clone git@github.com:julsql/config.git
cd config
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt 
```

Ajouter le fichier de configuration de l'API google sheet `private/bd-sheet-91.json`

### Configurer son téléphone

Ajouter le raccourci qui :

1. Scanne le code bar pour en récupérer l'ISBN
2. Exécute le script python sur la VM en s'y connectant en SSH
   > Ajouter la clef SSH su téléphone dans la VM au préalable
3. Affiche le message (erreur ou validé)

## Guide

Se connecter à la VM : guide pratique

### Clef SSH

Générer clef SSH

```bash
ssh-keygen -t rsa
```

Pour ne pas remettre le mot de passe de la VM à chaque fois : ajouter la clef SSH dans la VM

Dans la VM :

```bash
ssh user@address
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Sur son propre ordinateur

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub user@server
```

Ou bien ajouter la clef à partir de la VM directement :
(avec le fichier key qui contient la clef)

```bash
cat ~/key >> ~/.ssh/authorized_keys
```

## Auteur

Jul SQL
