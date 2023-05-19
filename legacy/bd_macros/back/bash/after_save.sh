#! /bin/bash

path="/path/to/project"

cd "$path"
git add *;
git commit -m "Save excel";
git push origin;