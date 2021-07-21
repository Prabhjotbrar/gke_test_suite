from marshmallow_dataclass import class_schema, marshmallow
from dataclasses import dataclass
import sys
import yaml
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

@dataclass
class spm_config:
    host: str
    password: str
    username: str = 'admin'
    cluster: str = ''
    service_name: str = ''
    service_list: str = ''
    hours: int = 3
    output: str = f"./output-{timestr}.csv"
    debug: bool = False

def read_config_yaml(filename):
    try:
        schema = class_schema(spm_config)
        with open(filename) as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
            return schema().load(config)
    except marshmallow.exceptions.ValidationError as e:
        print("Validation errors in the configuration file.")
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        print("Unable to read the config file.")
        sys.exit(1)