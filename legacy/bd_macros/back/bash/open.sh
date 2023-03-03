#! /bin/bash

cd "/path/to/project";
git pull;

#value=$(cat back/bash/changes.txt)
# Vérification de la valeur
#echo $value
#if [ $value -eq "1" ]
#then
python3 "back/update_xlsm.py";
    #rm "back/bash/changes.txt"; touch "back/bash/changes.txt";
    #echo 0 >> "back/bash/changes.txt";
    #sleep 1
open -a "/Applications/Microsoft Excel.app" BD.xlsm;
#fi