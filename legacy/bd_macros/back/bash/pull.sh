#! /bin/bash

path="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"

cd "$path";
git pull;