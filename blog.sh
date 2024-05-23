#!/bin/sh
echo $1
if [ "$1" == "init" ]
then
   echo "Initializing the blog post"
   python3 _init.py "$2"
fi

if [ "$1" == "update" ]
then
    echo "Building $2"
    scp -r "blogposts/$2" "jekyll/"
    jekyll build -s "jekyll/" -d "output/$2"
    mv output/$2/$2/* output/$2/
    rm -rf "jekyll/$2"
    rm -rf output/$2/$2
    indexHtml=;
    echo $indexHtml
    python3 "_update.py" "$(pwd)/output/$2/index.html" "$2"
fi