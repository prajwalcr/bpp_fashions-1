kubectl get service
kubectl get pod -l service=postgres -o jsonpath="{.items[0].metadata.name}"
kubectl get pod -l service=flask -o jsonpath="{.items[0].metadata.name}"
POD_NAME=$(kubectl get pod -l service=flask -o jsonpath="{.items[0].metadata.name}")
kubectl exec $POD_NAME --stdin -- pytest