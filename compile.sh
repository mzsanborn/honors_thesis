#!/bin/bash
set -e

# Build image
docker build --platform linux/amd64 -t spatialsoft2d-x86_64 .

# Remove container if it exists
docker rm -f temp_container 2>/dev/null || true

# Create container
docker create --name temp_container spatialsoft2d-x86_64 

# Copy binary out
docker cp temp_container:/app/spatialsoft2d ./spatialsoft2d

# Copy to remote server
scp spatialsoft2d miazsanborn@ap41.uw.osg-htc.org:/home/miazsanborn/thesis/executables

#to use: chmod +x compile.sh  (if changed)
#./compile.sh 