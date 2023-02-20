POD_NAME=$(kubectl get pod -l app=flask -o jsonpath="{.items[0].metadata.name}")
echo $POD_NAME container found
kubectl exec $POD_NAME --stdin -- pytest