#! /bin/bash

path="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"

echo 0 > "$path/back/bashchanges.txt";