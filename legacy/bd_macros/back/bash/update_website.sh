#! /bin/bash

BACK_PATH="/path/to/project/back"

/opt/homebrew/bin/python3 "$BACK_PATH/xlsx2sql.py"
sqlite3 "$BACK_PATH/db.sqlite3" < "$BACK_PATH/BD.sql"