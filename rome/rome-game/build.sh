#!/bin/bash

echo "running script"

which npm
echo "node version $(node -v)"
echo "npm version $(npm -v)"

picked=$1
echo "running script with picked number: $picked"

rm rome-game/assets/minion.png
mv small_${picked}.png rome-game/assets/minion.png

cd rome-game
echo "cwd $(pwd)"

npm run build --verbose

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