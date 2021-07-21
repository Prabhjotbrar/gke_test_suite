#!/usr/bin/env bash
while true
do
printf "Checking the pod status in tsb namespace \n"
if [ $(kubectl get pods -n tsb | grep -v Running | grep -v Completed  | awk '{if(NR>1)print}' | wc -l) -eq 0 ]; then
  printf  "TSB control plane is up \n"
  sleep 2
 
else
  printf  "TSB control plane is not up, Please check the pod status \n"
  break
fi

printf "Checking the pod status in istio-system namespace \n"
if [ $(kubectl get pods -n istio-system | grep -v Running | grep -v Completed | grep false -c) -eq 0 ]; then 
  printf  "TSB control plane is up\n"
  sleep 2
else
  printf  "Istio  control plane is not up, Please check the pod status\n"
  break
fi

printf "Checking the pod status in istio-gateway  namespace \n"
if [ $(kubectl get pods -n istio-gateway | grep -v Running | grep -v Completed | grep false -c) -eq 0 ]
then
  printf  "Deploymemt is up\n"
  sleep 1
  break
else
  printf  "istio-gateway  is not up"
  break
fi
done
