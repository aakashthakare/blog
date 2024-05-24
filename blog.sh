#!/bin/sh
blogpost=$1

if [[ "$blogpost" == draft/* ]]; then
    blogpost=$(echo "$blogpost" | sed 's/^draft\///')
fi

DIR="blogposts/$blogpost"
IS_INIT=$([ -d "$DIR" ] && echo 1 || echo 0)

if [ $IS_INIT == 0 ];
then
   echo "Initializing $blogpost..."
   python3 _blogops.py init "$blogpost"
else
    echo "Updating $blogpost..."
    scp -r "blogposts/$blogpost" "jekyll/"
    jekyll build -s "jekyll/" -d "output/$blogpost"
    if [ -f output/$blogpost/$blogpost/* ]; then
        mv output/$blogpost/$blogpost/* output/$blogpost/
    fi
    rm -rf "jekyll/$blogpost"
    rm -rf output/$blogpost/$blogpost
    indexHtml=;
    echo $indexHtml
    python3 _blogops.py update "$(pwd)/output/$blogpost/index.html" "$blogpost"
fi