#! /bin/bash

cd /path/to/bd/;
git pull;
python3 /path/to/bd/back/ajout_tableur.py $1;
rm "back/bash/changes.txt"; touch "back/bash/changes.txt";
echo "1" > "back/bash/changes.txt";
git add *;
git commit -m "add isbn ${1}";
git push origin;