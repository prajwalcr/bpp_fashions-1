#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ./kubernetes/persistent-volume.yml
kubectl apply -f ./kubernetes/persistent-volume-claim.yml


echo "Creating credentials..."

kubectl apply -f ./kubernetes/secret.yml


echo "Creating environment..."

kubectl apply -f ./kubernetes/env-configmap.yml


echo "Creating the postgres deployment and service..."

kubectl create -f ./kubernetes/postgres-deployment.yml
kubectl create -f ./kubernetes/postgres-service.yml
sleep 45
POD_NAME=$(kubectl get pod -l service=postgres -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD_NAME --stdin --tty -- createdb -U unbxd bpp


echo "Creating the redis deployment and service"

kubectl create -f ./kubernetes/redis-deployment.yml
kubectl create -f ./kubernetes/redis-service.yml


echo "Creating the flask deployment and service..."

kubectl create -f ./kubernetes/flaskapp-deployment.yml
kubectl create -f ./kubernetes/flaskapp-service.yml


echo "Adding the ingress..."

kubectl apply -f ./kubernetes/ingress.yml


echo "Creating the frontend deployment and service..."

kubectl create -f ./kubernetes/frontend-deployment.yml
kubectl create -f ./kubernetes/frontend-service.yml