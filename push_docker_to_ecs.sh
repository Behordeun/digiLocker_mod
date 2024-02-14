#!/usr/bin/env bash
# This file tags and uploads an image to AWS ECR

# Assumes that an image is built via `run_docker.sh`

# Step 1:
# Login into ECR

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992008361880.dkr.ecr.us-east-1.amazonaws.com/digilocker
# Step 2:
# Build the image
docker build -t digilocker .

# Step 3:
#  Tag the image
docker tag digilocker:latest 992008361880.dkr.ecr.us-east-1.amazonaws.com/digilocker

# Step 4:
# Push the image to ECR
docker push 992008361880.dkr.ecr.us-east-1.amazonaws.com/digilocker
