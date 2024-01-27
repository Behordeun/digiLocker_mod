#!/usr/bin/env bash

#This is your Docker ID/path
dockerpath=herbehordeun/digilocker-mod
imageTag=latest

# Run the Docker Hub container with kubernetes
kubectl run digilocker-mod --image=$dockerpath:$imageTag --port=8083 --labels app=digilocker-mod

# List kubernetes pods
kubectl get pods

# Forward the container port to a host
kubectl port-forward digilocker-mod 8083:8083
