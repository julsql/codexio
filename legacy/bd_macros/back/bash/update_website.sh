#! /bin/bash

git pull
BACK_PATH="/path/to/bd_database/back"

rm "$BACK_PATH/db.sqlite3"
/usr/bin/python3 "$BACK_PATH/xlsx2sql.py"
sqlite3 "$BACK_PATH/db.sqlite3" ".read $BACK_PATH/BD.sql"
cp "$BACK_PATH/db.sqlite3" ~/bd/bd/db.sqlite3
cat "$BACK_PATH/bash/password" | sudo -S service apache2 restart

