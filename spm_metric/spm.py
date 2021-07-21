import json
import sys
import datetime
import requests
import logging
import spm_helpers

logger = logging.getLogger(__name__)

def get_services(username, password, url, service_name='', cluster='') :
    # TO-DO: rewrite the logic and name the function get filtered services.
    # In the filter supply the values like service_name and cluster
    logger.info("*** Getting all services from tsb ***")
    #services will fetched for today
    today = str(datetime.date.today())

    # need to make this pass as command line arg or from the calling script
    header = {'Content-Type': 'application/json'}
    start_date = f'"{today}"'
    end_date = f'"{today}"'
    if(service_name == ''):
        raw_data = spm_helpers.get_services_query(start_date, end_date)
    else:
        raw_data = spm_helpers.get_services_by_name_query(start_date, end_date, service_name)
    
    res=""

    try:
        res = requests.post(url, verify=False, headers=header, auth=(username,password), data=raw_data)
    except:
        logger.info(f'*** {sys.exc_info()[0]} ***')
        logger.error('*** Fetching service Ids from the setup failed***')
        
    service_list=[]

    if res.status_code == 200 :
        res_json = json.loads(res.content)
        if 'errors' in res_json: 
            sys.exit(res_json['errors'])
        for x in res_json["data"]["services"]:
            label_array = x["label"].split('|')
            if(len(label_array)<4) :
                logger.info(f'Unknown label {x["label"]}')
                continue
            if cluster != '':
                if label_array[-2] == cluster:
                    # if x["label"].startswith("*") and x["label"].endswith("-"):
                    service_list.append(x)
            else:
                # if x["label"].startswith("*") and x["label"].endswith("-"):
                service_list.append(x)
    else :
        logger.error("*** Fetching service Ids from the setup failed***")

    logger.info(f'*** Number of services to check is {len(service_list)} ***')

    return service_list

def validate_services(service_file, services):
    service_names = []
    missing_services = []
    for value in services:
        service_names.append(value['label'])
    with open(service_file) as file:
        lines = file.read().splitlines()
        for line in lines:
            if line == '':
                continue
            if line not in service_names:
                missing_services.append(line)
    return missing_services
                


def check_service_metrics(username, password, hours, service, url) :

    logger.debug(f'*** Getting the service metrics for service id {service["label"]} ***')

    fetch_error = 1

    start_time, end_time = spm_helpers.get_time_limits(hours)

    # need to make this pass as command line arg or from the calling script
    header = {'Content-Type': 'application/json'}
    service_id='\"'+service["key"]+'\"'
    query= spm_helpers.get_metrics_query(start_time, end_time, service_id)

    logger.debug(f"Check_service_metrics query : {query}")

    res=""

    logging.getLogger("requests").setLevel(logging.ERROR)

    try:
        res = requests.post(url, verify=False, headers=header, auth=(username,password),data=query)
    except:
        logger.debug(f'*** {sys.exc_info()[0]} ***')
        logger.error(f'*** Fetching metrics for Service Id {service} failed***')
        fetch_error = 0

    res_value=str(res)
    data_error = 0
    csv_response = []
    if "200" in res_value :
        json_response=json.loads(res.content)
        logger.debug(f'*{json_response}*')
        csv_response,data_error = spm_helpers.create_csv(json_response, service)
    else :
        fetch_error = 0
        logger.error(f'*** Fetching metrics for Service Id {service} failed***')

    return fetch_error,data_error, csv_response

