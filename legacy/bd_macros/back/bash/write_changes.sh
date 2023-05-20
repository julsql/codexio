#! /bin/bash

path="/path/to/projectd"

cd "$path/back/bash";

rm "changes.txt"; touch "changes.txt";
echo 0 >> "changes.txt";