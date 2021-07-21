import argparse
import sys
import logging
import spm
import getpass
import tqdm
import urllib3
import csv
import spm_helpers
import time
import config
timestr = time.strftime("%Y%m%d-%H%M%S")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global logger

def main() :
    args = parse_args()
    # TO-DO - create a seprate function to validate all the user inputs
    if args.password is None:
        args.password = getpass.getpass(prompt='Password:')
    
    if not args.output.endswith('.csv'):
        sys.exit(f"Expected output file extention to be `.csv` but got - {args.output}")
    
    graphql_url = f'https://{args.host}/graphql'
    
    # set log level
    log_level =  logging.DEBUG if args.debug else logging.INFO 
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    # get services by name or get all by supplying empty service_name
    services = spm.get_services(args.username, args.password, graphql_url, service_name=args.service_name, cluster=args.cluster)

    # validate the services against list of services supplied.
    missing_services = []
    if args.service_list != '':
        missing_services = spm.validate_services(args.service_list, services)

    flag_error_counter = 0
    data_error_counter = 0
    hoursHeader = spm_helpers.create_header_name_for_each_hour(args.hours)

    with open(args.output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Metrics Name',*hoursHeader, 'Status', 'Subset','Service Name/Hostname', 'Namespace', 'Cluster', 'Env'])
        csv_response = []
        for service in tqdm.tqdm(services, desc=f'Fetching metrics for {len(services)} services...') :
            fetch_error,data_error,rows = spm.check_service_metrics(args.username, args.password, args.hours, service, graphql_url)
            csv_response += rows
            if fetch_error == 0 :
                flag_error_counter+=1
                logger.error(f'*** Fetching metrics for Service Id { service["key"] } failed***')
                break
            if data_error > 0 :
                data_error_counter+=1
        for missing_service in missing_services:
                row, _ = spm_helpers.prepare_row({}, 'N/A', missing_service, args.hours)
                csv_response.append(row)
        for row in csv_response:
            writer.writerow(row)


    logger.info(f'*** Total number of services is {len(services)} ***')
    logger.info(f'*** Total number of services which failed to collect metrics {flag_error_counter} ***')
    logger.info(f'*** Total number of metrics with all non-zero values {len(services) - data_error_counter} ***')


def parse_args():
    parser = argparse.ArgumentParser(
        description="This tool is for fetching SPM metrics for TSB and write them into a CSV.\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )


    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--host",
        help="TSB domain name or IP and port number. e.g. 1.2.3.4:9999"
    )

    group.add_argument(
        "--config", 
        help="pass the config file instead of arguments."
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Output file path. Default path is `./output-YYYYMMDD-HHMMSS.csv`.",
        default=f"./output-{timestr}.csv"
    )

    parser.add_argument(
        "--username",
        "-u",
        help="Username of TSB instance. Default is admin.",
        default="admin"
    )

    parser.add_argument(
        "--password",
        "-p",
        help="Password of TSB instance.",
    )

    parser.add_argument(
        "--hours",
        help="How many hours of you data you want to fetch.",
        type=int,
        default=3
    )

    parser.add_argument(
        "--service-name",
        "-n",
        help="Filter the service metrics by service name.",
        default=''
    )

    parser.add_argument(
        "--service-list",
        "-s",
        help="A file containing list of services that must exists in the spm output. If the services do not exist, we will log an error.",
        default='',
    )

    parser.add_argument(
        "--cluster",
        "-c",
        help="Cluster name for which you want to fetch the metrics. By default it fetches for all the clusters.",
        default='',
    )

    parser.add_argument(
        "--debug",
        help="Enable debug logs.",
        action="store_true"
    )
    
    args = parser.parse_args()

    final_args = args
    if args.config:
        final_args = config.read_config_yaml(args.config)
    return final_args

        
###########

if __name__ == '__main__':
    main()
