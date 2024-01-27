#!/usr/bin/env bash
# Step 1:
# Login into ECR

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992008361880.dkr.ecr.us-east-1.amazonaws.com

# Step 2:
# Build the image
docker build -t digilocker-mod .

# Step 3:
#  Tag the image
docker tag digilocker-mod:digilocker_heroku 992008361880.dkr.ecr.us-east-1.amazonaws.com/digilocker:digilocker_heroku

# Step 4:
# Push the image to ECR
docker push 992008361880.dkr.ecr.us-east-1.amazonaws.com/digilocker:digilocker_heroku
