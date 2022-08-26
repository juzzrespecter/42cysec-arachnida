#!/bin/bash

IMG_NAME="arachnida"

docker build -t ${IMG_NAME}:latest
docker run \
       -it \
       --name ${IMG_NAME} \
       --rm \
       ${IMG_NAME}:latest \
       /bin/sh
