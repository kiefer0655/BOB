
import yaml
import sys

def load_config(filename='config.yaml'):
    with open(filename, 'r') as file:
        try:
            # Use safe_load to avoid arbitrary code execution from untrusted sources
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            return sys.exit(1)
        
CONFIG = load_config()
print("CONFIG LOADED")