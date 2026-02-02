Prueba
kubectl exec -it <nombre-pod-redis> -- sh
redis-cli set mi_dato "hola mundo"
kubectl delete pod <nombre-pod-redis>

redis-cli get mi_dato.