#! /bin/bash

BACK_PATH="/path/to/bd_database/back"
cd $BACK_PATH

git pull

rm "$BACK_PATH/db.sqlite3"
/usr/bin/python3 "$BACK_PATH/xlsm2sql.py"
sqlite3 "$BACK_PATH/db.sqlite3" ".read $BACK_PATH/BD.sql"
cp "$BACK_PATH/db.sqlite3" ~/bd/bd/db.sqlite3
cat "$BACK_PATH/bash/password" | sudo -S service apache2 restart
git add "$BACK_PATH/BD.xlsx"
git commit -m "updating website"
git push
