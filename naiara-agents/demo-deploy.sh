#!/bin/bash

export AWS_PROFILE=Aia

aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 135808953483.dkr.ecr.eu-west-3.amazonaws.com

docker buildx build --platform linux/amd64 -t demo/naiara-agents .

docker tag demo/naiara-agents:latest 135808953483.dkr.ecr.eu-west-3.amazonaws.com/demo/naiara-agents:latest

docker push 135808953483.dkr.ecr.eu-west-3.amazonaws.com/demo/naiara-agents:latest

kubectl delete pods -n demo -l app=naiara-agents-service-demo
