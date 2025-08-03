#!/bin/sh

blogposttitle=$1

git checkout -b draft/$blogposttitle 
git push -u origin draft/$blogposttitle

echo "Waiting for GitHub Action to create and commit the post files."
sleep 150

git pull --rebase