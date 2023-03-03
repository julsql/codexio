#! /bin/bash

cd /path/to/bd/;
git pull;
python3 /path/to/bd/back/ajout_tableur.py $1;
git add *;
git commit -m "add isbn ${1}";
git push origin;
