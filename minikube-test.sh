POD_NAME=$(kubectl get pod -l service=flaskapp -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD_NAME --stdin -- pytest