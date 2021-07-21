#!/bin/bash

kubectl create ns n1
kubectl apply -f <(istioctl kube-inject -f manifest/httpbin.yaml) -n n1
kubectl apply -f <(istioctl kube-inject -f manifest/sleep.yaml) -n n1
kubectl create ns n2
kubectl apply -f <(istioctl kube-inject -f manifest/httpbin.yaml) -n n2
kubectl apply -f <(istioctl kube-inject -f manifest/sleep.yaml) -n n2

echo "Waiting for deployment to come up"
sleep 10

for from in "n1" "n2" ; do for to in "n1" "n2" ; do kubectl exec "$(kubectl get pod -l app=sleep -n ${from} -o jsonpath={.items..metadata.name})" -c sleep -n ${from} -- curl -s "http://httpbin.${to}:8000/ip" -s -o /dev/null -w "sleep.${from} to httpbin.${to}: %{http_code}\n"; done; done
