#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
docker build -t digilocker-mod:digilocker_heroku .

# Step 2:
docker images

# Step 3:
docker run -p 8083:8083 digilocker-mod:digilocker_heroku
