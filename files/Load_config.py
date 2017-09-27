import json
import os

#config_path = "/home/student/Pyc/lab2/config.json"
#config_path = os.path.join('files', 'config.json')
os.path.abspath("".join("config.json"))
config_path = "/home/student/lab3/config.json"

def Load_config(path = config_path):
    with open(config_path) as json_config:
        data = json.load(json_config)
    return data