#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# Assumes that an image is built via `run_docker.sh`

# Step 1:
# Create dockerpath
dockerpath=herbehordeun/digilocker-mod

# Step 2:
# Authenticate & tag
docker login --username=herbehordeun
docker image tag digilocker-mod $dockerpath
echo "Docker ID and Image: $dockerpath"

# Step 3:
docker push $dockerpath:latest
