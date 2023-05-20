#! /bin/bash

path="/path/to/project"

cd "$path/back/bash";

rm "changes.txt"; touch "changes.txt";
echo 0 >> "changes.txt";