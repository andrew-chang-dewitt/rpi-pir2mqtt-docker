import yaml

obj = {}

with open("configuration.yaml", 'r') as stream:
    try:
        obj = yaml.safe_load(stream)
    except:
        raise

print(obj)
