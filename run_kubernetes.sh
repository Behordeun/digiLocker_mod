#!/usr/bin/env bash

#This is your Docker ID/path
dockerpath=herbehordeun/digilocker
imageTag=latest

# Run the Docker Hub container with kubernetes
kubectl run digilocker --image=$dockerpath:$imageTag --port=8083 --labels app=digilocker

# List kubernetes pods
kubectl get pods

# Forward the container port to a host
kubectl port-forward digilocker 8083:8083
