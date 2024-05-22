#!/bin/sh
echo "Building $1"
scp -r "blogposts/$1" "jekyll/"
jekyll build -s "jekyll/" -d "output/$1"
mv output/$1/$1/* output/$1/
rm -rf "jekyll/$1"
rm -rf output/$1/$1
echo file://"$(pwd)/output/$1/index.html"