import datetime
import sys

metrics_details = {
 "throughput": {
     "validation_type": "range",
     "min_value" : 1,
     "max_value" : sys.maxsize,
     "unit": "rpm"

 },
 "response_time": {
     "validation_type": "range",
     "min_value" : 1,
     "max_value" : 200,
     "unit": "ms"
 },
 "service_2xx": {
     "validation_type": "range",
     "min_value" : 1,
     "max_value" : sys.maxsize,
     "unit": "rpm"
 },
 "service_4xx": {
     "validation_type": "constant",
     "value" : 0,
     "unit": "rpm"
 },
 "service_5xx": {
     "validation_type": "constant",
     "value" : 0,
     "unit": "rpm"
 },
}

def get_metrics_query(start_tick, end_tick, service_id):
    return f'''
    {{ 
        "query": "query WidgetQuery($duration: Duration!, $serviceId: ID!) {{
            throughput: getLinearIntValues(metric: {{name: \\"service_cpm\\", id: $serviceId}}, duration: $duration) 
            {{
                values {{ value }}
            }},
            response_time: getLinearIntValues(metric: {{name: \\"service_resp_time\\", id: $serviceId}}, duration: $duration) 
            {{
                values {{ value }}
            }},
            service_2xx: getLinearIntValues(metric: {{name: \\"service_2xx\\", id: $serviceId}}, duration: $duration) 
            {{
                values {{ value }}
            }},
            service_4xx: getLinearIntValues(metric: {{name: \\"service_4xx\\", id: $serviceId}}, duration: $duration) 
            {{
                values {{ value }}
            }}
            service_5xx: getLinearIntValues(metric: {{name: \\"service_5xx\\", id: $serviceId}}, duration: $duration) 
            {{
                values {{ value }}
            }}
        }}",
        "variables": {{
            "duration": {{
                "start":{start_tick},
                "end":{end_tick},
                "step":"HOUR"
                }},
            "serviceId": {service_id}
            }}
    }}
    '''


def get_services_query(start_date, end_date):
    return f'''
    {{ 
        "query": "query queryServices($duration: Duration!) 
            {{
                services:getAllServices(duration: $duration) {{
                    key: id,
                    label: name
                    }}
            }}",
        "variables": {{
            "duration": {{
                "start": {start_date},
                "end": {end_date},
                "step": "HOUR"
                }}
            }}
    }}'''

def get_services_by_name_query(start_date, end_date, service_name):
    return f'''
    {{
        "query": "query queryServices($duration: Duration!, $service_name: String!)
        {{
            services: searchServices(duration: $duration, keyword: $service_name){{
                key: id,
                label: name
            }}
        }}",
        "variables": 
        {{
            "duration": {{
                "start": {start_date},
                "end": {end_date},
                "step": "DAY"
                }},
            "service_name": "{service_name}"
        }}
    }}'''

def create_csv(json_response, service):
    '''
    This function creates the CSV output from the json response and services
    How it's done?
    For each type of metrics in `json_response` it will create a new row. `service` information will be common for all the rows because
    these are different metrices for the same service.
    '''
    data_error = 0
    csv_response = []
    for metric_name in ['throughput', 'response_time', 'service_2xx', 'service_4xx', 'service_5xx']:
        row,error = prepare_row(json_response, metric_name, service['label'])
        data_error += error
        csv_response.append(row)
    return csv_response,data_error

def prepare_row(json_response, metric_name, service, hours=0):
    '''
    prepare a single row data for a given metric from json_response.
    the last argument hours is required only in case of adding missing services for which we do not have metrics.
    '''
    data_error = 0
    row = [f"{metric_name} ({metrics_details[metric_name]['unit']})"] if metric_name != 'N/A' else ['N/A']
    # json response will be blank only in case of adding missing services.
    if json_response != {}:
        for x in json_response['data'][metric_name]['values'] :
            # if metrics value is not in a given range or is not equal to a contant as per the expacted values for a given metric then it's data error.
            if ((metrics_details[metric_name]['validation_type'] == 'range' and not metrics_details[metric_name]['min_value'] <= x['value'] <= metrics_details[metric_name]['max_value'])
                or (metrics_details[metric_name]['validation_type'] == 'constant' and metrics_details[metric_name]['value'] != x['value'])):
                data_error+=1
            row.append(x['value'])
        row.append('Not OK' if data_error > 0 else 'OK')
    else:
        # adding missing services
        # 1. append '-' in place of hours as the service was not found in SMP so no metrics in available.
        for i in range(hours):
            row.append('N/A')
        # 2. adding status as 'Not OK'
        row.append('Service ID missing')
    service_details = service.split('|')
    if len(service_details) == 4:
        row = row + ['-'] + service_details
    else:
        row = row + service_details

    return row, data_error


def get_time_limits(hours=3):
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(hours=hours-1)
    end = now 

    start_tick = f'"{start:%Y-%m-%d %H}"'
    end_tick = f'"{end:%Y-%m-%d %H}"'
    return start_tick,end_tick


def create_header_name_for_each_hour(hours=3):
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(hours=hours-1)
    end = now 
    hours_header = []
    while(start.hour <= end.hour):
        hours_header.append(f"{start.hour}:00")
        start += datetime.timedelta(hours=1)
    return hours_header