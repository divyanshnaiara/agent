#!/bin/bash

export AWS_PROFILE=Aia

aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 135808953483.dkr.ecr.eu-west-3.amazonaws.com

docker buildx build --platform linux/amd64 -t dev/naiara-agents .

docker tag dev/naiara-agents:latest 135808953483.dkr.ecr.eu-west-3.amazonaws.com/dev/naiara-agents:latest

docker push 135808953483.dkr.ecr.eu-west-3.amazonaws.com/dev/naiara-agents:latest

kubectl delete pods -n dev -l app=naiara-agents-service-dev
