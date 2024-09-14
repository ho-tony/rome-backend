#!/bin/bash

npm run build

# Exit immediately if a command exits with a non-zero status
set -e

# Create the ./dist/maps directory if it doesn't already exist
mkdir -p ./dist/maps

# Copy everything from ./public/maps to ./dist/maps
cp -r ./public/maps/* ./dist/maps/

# Copy ./dist_index.html to ./dist/index.html
cp ./dist_index.html ./dist/index.html

# Zip up the ./dist folder into a file called dist.zip in the current directory
zip -r ./dist.zip ./dist