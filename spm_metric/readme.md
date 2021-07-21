# SPM Testing Scripts/Tool 
This tool is for fetching metrics information form SPM (Skywalking path metrics) for a given TSB instance. The output of this tool is a CSV file, which will look something like this

| Metrics Name  | 1st hour | 2nd hour | Status | Hostname/Subset | Service Name | Namespace        | Cluster | Env |
|---------------|----------|----------|--------|-----------------|--------------|------------------|---------|-----|
| throughput    | 2        | 2        | OK     | *               | ratings-1    | t0w0demobkifnb0f | *       | -   |
| response_time | 1        | 1        | OK     | *               | ratings-1    | t0w0demobkifnb0f | *       | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-1    | t0w0demobkifnb0f | *       | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-1    | t0w0demobkifnb0f | *       | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-1    | t0w0demobkifnb0f | *       | -   |
| throughput    | 2        | 2        | OK     | *               | ratings-2    | t0w0demobkifnb0f | *       | -   |
| response_time | 1        | 1        | OK     | *               | ratings-2    | t0w0demobkifnb0f | *       | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-2    | t0w0demobkifnb0f | *       | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-2    | t0w0demobkifnb0f | *       | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-2    | t0w0demobkifnb0f | *       | -   |
| throughput    | 2        | 2        | OK     | *               | ratings-0    | t0w0demobkifnb0f | *       | -   |
| response_time | 1        | 1        | OK     | *               | ratings-0    | t0w0demobkifnb0f | *       | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-0    | t0w0demobkifnb0f | *       | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-0    | t0w0demobkifnb0f | *       | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-0    | t0w0demobkifnb0f | *       | -   |
| throughput    | 2        | 2        | OK     | *               | ratings-2    | t0w0demobkifnb0f | demo    | -   |
| response_time | 1        | 1        | OK     | *               | ratings-2    | t0w0demobkifnb0f | demo    | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-2    | t0w0demobkifnb0f | demo    | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-2    | t0w0demobkifnb0f | demo    | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-2    | t0w0demobkifnb0f | demo    | -   |
| throughput    | 2        | 2        | OK     | *               | ratings-1    | t0w0demobkifnb0f | demo    | -   |
| response_time | 1        | 1        | OK     | *               | ratings-1    | t0w0demobkifnb0f | demo    | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-1    | t0w0demobkifnb0f | demo    | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-1    | t0w0demobkifnb0f | demo    | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-1    | t0w0demobkifnb0f | demo    | -   |
| throughput    | 2        | 2        | OK     | *               | ratings-0    | t0w0demobkifnb0f | demo    | -   |
| response_time | 1        | 1        | OK     | *               | ratings-0    | t0w0demobkifnb0f | demo    | -   |
| service_2xx   | 2        | 2        | OK     | *               | ratings-0    | t0w0demobkifnb0f | demo    | -   |
| service_4xx   | 0        | 0        | OK     | *               | ratings-0    | t0w0demobkifnb0f | demo    | -   |
| service_5xx   | 0        | 0        | OK     | *               | ratings-0    | t0w0demobkifnb0f | demo    | -   |


## Requirements
1. python3
2. pipenv

## Setup

```shell
pipenv shell
pipenv install
```

## Usages

command - 
```shell
python main.py --host x.x.x.x:port [--username][--password][--output][--hours][--service_name][--service-list][--debug]
```

| Command        | Abbreviation | Description                                                                      |
|----------------|--------------|----------------------------------------------------------------------------------|
| --host  |              | TSB domain name or IP and port number. e.g. 1.2.3.4:9999                         |
| --output       | -o           | Output file path. Default path is `./output-YYYYMMDD-HHMMSS.csv`.                |
| --username     | -u           | Username of TSB instance. Default is admin.                                      |
| --password     | -p           | Password of TSB instance. If you don't supply the password you will be prompted to type the password.|
| --hours        |              | How many hours of you data you want to fetch. Default is 3.                      |
| --service-name | -n           | Filter the service metrics by service name. By Default includes all the services.|
| --service-list | -s           | A file containing list of services that must exists in the spm output. If the services do not exist, we will log an error.|
| --debug        |              | Enable debug logs.                                                               |
| --config       |              | Path to config file to get all the arguments instead of command line.            |

If **--config** argument is passed all then all the other argument's value will be taken from the config file. Config file should be a yaml file like this one (yaml keys are same as command name in the above list):

```yaml
---
host: "1.2.3.4:8443"
password: "your-password"
username: 'admin'
cluster: 'demo'
service_name: 'productpage'
service_list: './spm-services.txt'
hours: 3
output: "./output.csv"
debug: False
```
