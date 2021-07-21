Steps to run the scripts

1. git clone https://github.com/Prabhjotbrar/gke_test_suite.git

2. cd gke_test_suite 

3. chmod +x  deployment_check.sh sample_deploy.sh

4. bash deployment_check.sh

the script will not complete unless there are some non-running/error pods

5. bash sample_deploy.sh

the script will deploy load_generating, httpbin and sleep application in 2 different namespaces and then query the svc endpoints. we should see http 200 response code.

6. cd spm_metric 

7. pipenv shell ; pipenv install

- Optional- it collects hourly metrics, please run this script after 2hrs after generating the traffic.-
8. Create a config file with yaml extension and fill out the below content.


host: "1.2.3.4:8443"
password: "your-password"
username: 'admin'
cluster: 'demo'
service_name: 'httpbin'
service_list: ''
hours: 2
output: "./output.csv"
debug: False



9. python main.py --config <>.yaml

This script will query the central telemetry and check if the metric is getting populated. This will check for below metric and genrate a report in csv file.

1. throughput  in rpm
2. response_time in ms
3. service_2xx reponse
4. service_4xx reponse
5. service_5xx reponse


