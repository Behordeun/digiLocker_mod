#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
docker build -t digilocker:latest .

# Step 2:
docker images

# Step 3:
docker run -p 8083:8083 digilocker:latest
