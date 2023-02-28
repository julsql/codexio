#! /bin/bash

git pull;
python3 /path/to/bd/ajout_tableur.py $1;
git add *;
git commit -m "add isbn ${$1}";
git push origin;