#! /bin/bash

cd "/path/to/project";
git pull;
touch "back/dismiss_macros.txt";
#value=$(cat back/bash/changes.txt)
# Vérification de la valeur
#echo $value
#if [ $value -eq "1" ]
#then
/opt/homebrew/bin/python3 "back/update_xlsm.py";
#rm "back/bash/changes.txt"; touch "back/bash/changes.txt";
#echo 0 >> "back/bash/changes.txt";
#sleep 1
open -a "/Applications/Microsoft Excel.app" BD.xlsm;
rm "back/dismiss_macros.txt";
#fi