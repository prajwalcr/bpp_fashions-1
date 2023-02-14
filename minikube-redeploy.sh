#!/bin/bash


echo "Building docker images..."

docker build -t prajwalcr/frontend-flaskapp ./frontend
docker build -t prajwalcr/flaskapp ./backend


echo "Pushing docker images..."

docker push prajwalcr/frontend-flaskapp
docker push prajwalcr/flaskapp

echo "Updated kubernetes deployments..."

kubectl delete deploy frontend
kubectl delete deploy flask
kubectl create -f ./kubernetes/frontend-deployment.yml
kubectl create -f ./kubernetes/flaskapp-deployment.yml

echo "Done"