#!/usr/bin/env bash
echo "Removing cached python compiled files..."
find . -name \*pyc  | xargs  rm -fv
find . -name \*pyo | xargs  rm -fv
find . -name \*~  | xargs  rm -fv
find . -name __pycache__  | xargs  rm -rfv

echo "Removing outdated coverage files and caches..."
rm -rf coverage .coverage .cache

#clean up and reclaim docker storgage space
echo "Cleaning up and reclaiming docker storage space..."

docker rm $(docker ps -aq)
docker rmi $(docker images --filter dangling=true --quiet)

echo "Clean up done!"