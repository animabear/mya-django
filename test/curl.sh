#!/bin/bash

rm output/*

url1="http://127.0.0.1:8000/home/" # add more URLs here
url2="http://127.0.0.1:8000/jinja2/"

for i in {1..300}; do
    # run the curl job in the background so we can start another job
    # and disable the progress bar (-s)
    # echo (i%2)
    if ! ((i % 2)); then
       url=$url1
    else
       url=$url2
    fi

    echo "fetching $url"
    curl $url -o output/$i.html -s &
done
wait #wait for all background jobs to terminate

echo 'done'
md5 -q output/*.html | sort -u