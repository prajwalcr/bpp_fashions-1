#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ./kubernetes/persistent-volume.yml
kubectl apply -f ./kubernetes/persistent-volume-claim.yml

echo "Creating credentials..."

kubectl apply -f ./kubernetes/secret.yml


echo "Creating environment..."

kubectl apply -f ./kubernetes/env-configmap.yml


echo "Creating the postgres deployment and service..."


kubectl apply -f ./kubernetes/postgres-deployment.yml
kubectl apply -f ./kubernetes/postgres-service.yml
kubectl wait pod --for=condition=Ready -l service=postgres
POD_NAME=$(kubectl get pod -l service=postgres -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD_NAME --stdin -- createdb -U unbxd bpp


echo "Creating the redis deployment and service"

kubectl apply -f ./kubernetes/redis-deployment.yml
kubectl apply -f ./kubernetes/redis-service.yml


echo "Creating the flask deployment and service..."

kubectl apply -f ./kubernetes/flaskapp-deployment.yml
kubectl apply -f ./kubernetes/flaskapp-service.yml


echo "Creating the frontend deployment and service..."

kubectl apply -f ./kubernetes/frontend-deployment.yml
kubectl apply -f ./kubernetes/frontend-service.yml


echo "Adding the ingress..."

minikube addons enable ingress
kubectl apply -f ./kubernetes/ingress.yml



echo "Adding the ingress..."

kubectl apply -f ./kubernetes/ingress.yml


echo "Done"