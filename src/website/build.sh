#!/bin/sh
npx tailwindcss -i ./src/static/input.css -o ./src/static/output.css --minify
pipenv requirements > requirements.txt
docker build . -t n8website
