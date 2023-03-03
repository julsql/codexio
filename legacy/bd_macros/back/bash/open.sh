#! /bin/bash

cd "/path/to/project";
git pull;

value=$(cat back/bash/changes.txt)
# Vérification de la valeur
echo $value
if [ $value -eq "1" ]
then
    python3 "back/update_xlsm.py";
    echo 0 >> "back/bash/changes.txt"
else
  echo "La valeur est différente de 1"
fi

open -a /Applications/Microsoft\ Excel.app BD.xlsm;