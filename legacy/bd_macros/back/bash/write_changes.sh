#! /bin/bash

path="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"

cd "$path/back/bash";

echo 0 > "changes.txt";