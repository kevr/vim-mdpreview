#!/bin/bash

version="${1}.0"
echo $version > .tag
git add .tag
git commit -m "Add tag $1"

git tag -sa "$1"
